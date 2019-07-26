from ADCPi import ADCPi
import asyncio



class AdcDataSource():

    def __init(self, polling_rate = 10, address=0x68, address2=0x69, rate=18):
    
        self.adc = ADCPi(address, address2, rate)        
        self.channels = [1, 2, 3, 4, 5, 6, 7, 8]
        self.polling_rate = polling_rate
        
        self.running = False;
        self.data = []

    async start(self):
        return await self.main_loop()
        
    async def loop(self):
    
        while(self.running):
            
            data = {}            
            for ch in channels:                
                data[str(ch)] = self.adc.read_voltage(ch)
    
            self.data.append(data)            
            asyncio.sleep( 1.0 / self.polling_rate)