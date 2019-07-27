import gatt
from UUIDmappings import ser_to_name, char_to_name
import time

from BaseDataSource import BaseDataSource


class PolarDevice(gatt.Device):
    _UUID_SERVICE_DEV_INFO = '0000180a-0000-1000-8000-00805f9b34fb'
    _UUID_SERVICE_BATT = '0000180f-0000-1000-8000-00805f9b34fb'
    _UUID_SERVICE_HR = '0000180d-0000-1000-8000-00805f9b34fb'

    _UUID_CHARACTER_FIRMWARE_VER = '00002a26-0000-1000-8000-00805f9b34fb'
    _UUID_CHARACTER_BAT_LVL = '00002a19-0000-1000-8000-00805f9b34fb'
    _UUID_CHARACTER_HR_MEASURE = '00002a37-0000-1000-8000-00805f9b34fb'

    buff = []
    BUFF_SIZE = 300


    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))


    def print_out_services(self):
        """Walks through all self.servies printing out the uuids and their
        names. Should only be called *after* services_resolved() has been
        called."""
        print("RESOLVED SERVICES:")
        for s in self.services:
            print(s.uuid, "  " + ser_to_name.get(s.uuid[4:8], "Unknown"))
            if s.characteristics:
                for c in s.characteristics:
                    print(" -", c.uuid, char_to_name.get(c.uuid[4:8],
                          "Unknown"))

    def services_resolved(self):
        "Called after working out what services are offered"
        super().services_resolved()

        self.print_out_services()

        for s in self.services:
            if s.uuid == self._UUID_SERVICE_DEV_INFO:
                for c in s.characteristics:
                    if c.uuid == self._UUID_CHARACTER_FIRMWARE_VER:
                        c.read_value()
            elif s.uuid == self._UUID_SERVICE_BATT:
                for c in s.characteristics:
                    if c.uuid == self._UUID_CHARACTER_BAT_LVL:
                        c.read_value()
            elif s.uuid == self._UUID_SERVICE_HR:
                for c in s.characteristics:
                    if c.uuid == self._UUID_CHARACTER_HR_MEASURE:
                        c.enable_notifications()

    def characteristic_value_updated(self, characteristic, value):
        "Callback after reading a value or notification of value"
        if characteristic.uuid == self._UUID_CHARACTER_FIRMWARE_VER:
            print("Firmware version:", value.decode("utf-8"))
        elif characteristic.uuid == self._UUID_CHARACTER_BAT_LVL:
            print("Battery level:", value[0])
        elif characteristic.uuid == self._UUID_CHARACTER_HR_MEASURE:
            # TODO: There is much more information. See example code.
            print("HR Rec:", value[1])
            self.register(value[1])
        else:
            print("Unrecognised value:", value, "from:", characteristic.uuid,
                  char_to_name.get(characteristic.uuid[4:8],
                                   "Char name unrecognised."))

    def register(self, val):
        self.buff.append(str(val) + ", "
                         + datetime.now().strftime("%H:%M:%S.%f"))
        if len(self.buff) > self.BUFF_SIZE:
            with open(datetime.now().strftime("%H-%H-%S.%f") + ".csv",
                      "w") as fh:
                fh.write("\n".join(self.buff))
            self.buff = []

class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))



class PolarDataSource(BaseDataSource):

    def __init__(self, mac_address):
        self.mac_address = mac_address
        
        self.manager = AnyDeviceManager(adapter_name='hci0')
        #manager.start_discovery()
        
        print("Powered: ", self.manager.is_adapter_powered)
        
        self.device = PolarDevice(mac_address=mac_address, manager=self.manager)
        device.connect()
        
        manager.run()
        
        BaseDataSource.__init__("Polar", 1)
        
       
    def get_data(self, clear_cache=False):
        if(clear_cache):
            data = self.data
            self.clear_cache()
            return data
        else:    
            return self.data
       
    async def main_loop(self):
        self.running = True 
        while(self.running):
            
            data = {}            
            for ch in self.channels:                
                data[[time.time(), str(ch)]] = self.adc.read_voltage(ch)
            
            self.data.append(data)            
            await asyncio.sleep( 1.0 / self.sample_rate)


