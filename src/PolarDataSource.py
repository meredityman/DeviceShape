from datetime import datetime
import asyncio
from bleak import BleakClient
from bleak.exc import  BleakError
from src.BaseDataSource import BaseDataSource

UUID_CHARACTER_BAT_LVL      = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_CHARACTER_HR_MEASURE   = ''

class PolarDataSource(BaseDataSource):

    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.connected = False
        
        self.hr_latest  = -1
        self.bat_latest = -1
        self.client = None
        
        super(PolarDataSource, self).__init__("Polar", 1)

    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))


    async def loop_setup(self):    
        if(self.mac_address == ""):
            print("No mac address set for Polar")
            return

        try:
            print("Polar ({}): try connect...".format(self.mac_address))
            self.client = BleakClient(self.mac_address)

            await self.client.__aenter__()
            await asyncio.wait_for(self.printServices(self.client), timeout=10)

            print("Polar ({}): connected".format(self.mac_address))
        except BleakError as e:
            print("Polar ({}): failed to connect\n{}".format(self.mac_address, e))

        try:
            self.connected = await self.client.is_connected()
        except:
            pass

        if(self.connected):
            await self.start_notify()

    async def start_notify(self):
        try:
            await self.client.start_notify(UUID_CHARACTER_HR_MEASURE, self.hr_handler)
            self.is_setup = True
        except BleakError as e:
            print(e)

            
    async def loop_work(self):    
        if(self.client is None) : return

        try:
           self.connected = await self.client.is_connected()
        except:
           pass

        if(not self.connected):
            await self.loop_setup() 
        else:
            self.bat_latest = await self.client.read_gatt_char(UUID_CHARACTER_BAT_LVL)
  
    def get_status_messages(self):
       return [
            ("/{}/connected/".format(self.name), self.connected),
            ("/{}/setup/".format(self.name)    , self.is_setup),
            ("/{}/hr/".format(self.name)       , self.hr_latest),
            ("/{}/battery/".format(self.name)  , self.bat_latest)        
        ]
        
    def hr_handler(self, sender, data):
        print("HR: {}".format(int(data[1])))
        self.hr_latest = int(data[1])
        self.data.append({ "HR" : (datetime.now(), self.hr_latest  )})
    
    async def printServices(self, client):
        for service in client.services:
            print("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                print(
                    "\t[Characteristic] {0}: ({1}) | Name: {2}, Value: {3} ".format(
                        char.uuid, ",".join(char.properties), char.description, value
                    )
                )
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    print(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )
