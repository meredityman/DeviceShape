import datetime
import asyncio
from bleak import BleakClient
from bleak.exc import  BleakError
from src.BaseDataSource import BaseDataSource

UUID_SERVICE_DEV_INFO = '0000180a-0000-1000-8000-00805f9b34fb'
UUID_SERVICE_BATT     = '0000180f-0000-1000-8000-00805f9b34fb'
UUID_SERVICE_HR       = '0000180d-0000-1000-8000-00805f9b34fb'

UUID_CHARACTER_FIRMWARE_VER = '00002a26-0000-1000-8000-00805f9b34fb'
UUID_CHARACTER_BAT_LVL      = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_CHARACTER_HR_MEASURE   = '00002a37-0000-1000-8000-00805f9b34fb'

class PolarDataSource(BaseDataSource):

    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.connected = False
        super(PolarDataSource, self).__init__("Polar", 1)

    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))


    async def loop_setup(self):    
        try:

            self.client = BleakClient(self.mac_address)

            await self.client.__aenter__()
            await self.printServices(self.client)

            self.is_setup = await self.client.is_connected() 

            await self.client.start_notify("00002a37-0000-1000-8000-00805f9b34fb", self.hr_handler)
            
            #print("Device connected: {}".format(self.is_setup))
        except BleakError:
            print("Device {} not found".format(self.mac_address))
            
    async def loop_work(self):    
        self.is_setup = await self.client.is_connected()
        
        if(not self.is_setup):
            await self.loop_setup() 
  

        
    def hr_handler(self, sender, data):
        #print("HR: {}".format(int(data[1])))
        self.data.append({ "HR" : (time.localtime(), int(data[1]) )})
    
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
