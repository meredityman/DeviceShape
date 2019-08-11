from datetime import datetime
import asyncio
from bleak import BleakClient
from bleak.exc import  BleakError
from src.BaseDataSource import BaseDataSource

UUID_CHARACTER_BAT_LVL      = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_CHARACTER_HR_MEASURE   = '00002a37-0000-1000-8000-00805f9b34fb'
UUID_PWM_CONTROL_POINT      = 'fb005c81-02e7-f387-1cad-8acd2d8df0c8'
UUID_PWM_DATA               = 'fb005c82-02e7-f387-1cad-8acd2d8df0c8'

class PolarDataSource(BaseDataSource):

    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.connected = False
        self.connecting = False
        self.hr_latest  = -1
        self.bat_latest = -1
        self.client = None
        
        super(PolarDataSource, self).__init__("Polar", 1)

    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))

                
    async def close(self):
        if(self.client is not None):
            print("Polar ({}): disconnecting".format(self.mac_address))
            self.client.disconnect()
        
    async def loop_setup(self):    
        if(self.mac_address == ""):
            print("No mac address set for Polar")
            return

        if(self.connecting == True):
            print("Already connecting")
            return

        self.connecting = True
        try:
            print("Polar ({}): try connect...".format(self.mac_address))
            self.client = BleakClient(self.mac_address)

            await self.client.__aenter__()
            #await self.printServices(self.client)
            print("Polar ({}): connected".format(self.mac_address))
        except BleakError as e:
            print("Polar ({}): failed to connect\n{}".format(self.mac_address, e))

        try:
            self.connected = await self.client.is_connected()
        except:
            pass

        if(self.connected):
            await self.start_notify()


        self.connecting = False

    def disconnect_handler(self):
        print("Polar ({}): disconnected".format(self.mac_address))
        self.connected = False

    async def start_notify(self):
            #await self.client.start_notify(UUID_PWN_DATA            , self.data_handler)

            await self.client.write_gatt_char(UUID_PWM_CONTROL_POINT, bytearray(b'\x01\x02'), response = True)

            await self.client.start_notify(UUID_CHARACTER_HR_MEASURE, self.hr_handler)
            await self.client.set_disconnected_callback(self.disconnect_handler)

            self.is_setup = True
            print("Polar ({}): setup".format(self.mac_address))
        
 

    async def loop_work(self):    
        if(self.client is None) : return

        self.connected = await self.client.is_connected()
 
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

    def data_handler(self, sender, data):
        print("hey")
        #print("Data: {}".format(data))

    
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
