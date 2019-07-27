from ADCPi import ADCPi
import asyncio



class AdcDataSource():

    sample_rates = {
    12 : 240,
    14 : 60,
    16 : 15,
    18 : 3.75
    }


    def __init__(self, sample_rate = 10, address=0x68, address2=0x69, rate=14):
        self.name = "ADC"
        self.adc = ADCPi(address, address2, rate)        
        self.channels = [1, 2, 3, 4, 5, 6, 7, 8]
        
        if rate in self.sample_rates:
            max_sample_rate = self.sample_rates[rate]
        else :
            print("bit rate {} not permitted".format(rate))
            rate = 16
        
        if(sample_rate > max_sample_rate):
            print("Requested sample rate too high")
            
        self.sample_rate = min(max_sample_rate, sample_rate)
        
        self.running = False;
        self.data = []
        
        print("ADC Setup")


    def clear_cache(self):
        self.data = []

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
                data[str(ch)] = self.adc.read_voltage(ch)
            
            print(data)
            self.data.append(data)            
            await asyncio.sleep( 1.0 / self.sample_rate)
