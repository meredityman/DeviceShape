import time
from bleak import BleakClient
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
        super(PolarDataSource, self).__init__("Polar", 1)

    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))


    def get_data(self, clear_cache=False):
        if(clear_cache):
            data = self.data
            self.clear_cache()
            return data
        else:    
            return self.data
       
    async def main_loop(self):
        self.running = True 
        
        async with BleakClient(self.mac_address) as client:
            await client.is_connected()

            svcs = await client.get_services()
            print("Services:", svcs)

            while(self.running):
                
                data = {}        
                
                await client.read_gatt_char(UUID_SERVICE_DEV_INFO)
                print(
                    "System ID: {0}".format(
                        ":".join(["{:02x}".format(x) for x in system_id[::-1]])
                    )
                )
                
                self.data.append(data)            
                await asyncio.sleep( 1.0 / self.sample_rate)


