from src.ADCPi import ADCPi
import asyncio
import time

from src.BaseDataSource import BaseDataSource

class AdcDataSource(BaseDataSource):

    sample_rates = {
    12 : 240,
    14 : 60,
    16 : 15,
    18 : 3.75
    }


    def __init__(self, sample_rate = 10, address=0x68, address2=0x6a, rate=14):
        self.adc = ADCPi(address, address2, rate)        
        self.channels = [1, 2, 3, 4, 5, 6, 7, 8]
        
        if rate in self.sample_rates:
            max_sample_rate = self.sample_rates[rate]
        else :
            print("bit rate {} not permitted".format(rate))
            rate = 16
        
        if(sample_rate > max_sample_rate):
            print("Requested sample rate too high")
            
        sample_rate = min(max_sample_rate, sample_rate)
        
        super(AdcDataSource, self).__init__("ADC", sample_rate)
        
        
    async def main_loop(self):
        self.running = True 
        while(self.running):
            
            data = {}            
            for ch in self.channels:                
                data[str(ch)] = (time.localtime(),  self.adc.read_voltage(ch))
            
            self.data.append(data)            
            await asyncio.sleep( 1.0 / self.sample_rate)
