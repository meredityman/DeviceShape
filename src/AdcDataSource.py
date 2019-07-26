from ADCPi import ADCPi
import asyncio



class AdcDataSource():

    def __init__(self, polling_rate = 10, address=0x68, address2=0x69, rate=18):
        self.name = "ADC"
        self.adc = ADCPi(address, address2, rate)        
        self.channels = [1, 2, 3, 4, 5, 6, 7, 8]
        self.polling_rate = polling_rate
        
        self.running = False;
        self.data = []

    async def  start(self):
        self.running = True   
        
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.main_loop())

        
    async def main_loop(self):
    
        while(self.running):
            
            data = {}            
            for ch in self.channels:                
                data[str(ch)] = self.adc.read_voltage(ch)
            
            print(data)
            self.data.append(data)            
            await asyncio.sleep( 1.0 / self.polling_rate)
