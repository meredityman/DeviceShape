from src.ADCPi import ADCPi
import asyncio
import time

from src.BaseDataSource import BaseDataSource

class AdcDataSource(BaseDataSource):

    bit_rates = {
    12 : 240,
    14 : 60,
    16 : 15,
    18 : 3.75
    }
    
    channels = [1, 2, 3, 4, 5, 6, 7, 8]


    def __init__(self, sample_rate = 10, address=0x68, address2=0x6a, bit_rate=14):
    
        try:    
            self.adc = ADCPi(address, address2, bit_rate)
            is_setup = True
            
        except OSError:
            print("I2C not found at address")
            is_setup = False
        
        sample_rate = self.validate_sample_rate(sample_rate, bit_rate)
        
        super(AdcDataSource, self).__init__("ADC", sample_rate, is_setup)
    
    def validate_sample_rate(self, sample_rate, bit_rate):
        if bit_rate in self.bit_rates:
            max_sample_rate = self.bit_rates[bit_rate]
        else :
            print("bit rate {} not permitted".format(bit_rate))
            bit_rate = 16
            max_sample_rate = self.bit_rates[bit_rate]
        
        if(sample_rate > max_sample_rate):
            print("Requested sample rate too high")
            
        return min(max_sample_rate, sample_rate)
     

    async def loop_setup(self): 
        pass
     
    async def loop_work(self):
        data = {}
        for ch in self.channels:                
            data[str(ch)] = (time.localtime(),  self.adc.read_voltage(ch))
        
        self.data.append(data)            
