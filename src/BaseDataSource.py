import asyncio
import time

class BaseDataSource():
    

    def __init__(self, name, sample_rate, is_setup = False) :
        self.name = name
        self.data = []
        self.running = False;
        self.sample_rate = sample_rate
        
        self.is_setup = is_setup        
 
        if( self.is_setup ):
            print("{} Setup".format(self.name))
        else:
            print("{} Not Setup".format(self.name))

        
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
        
            data = {
                "X" : [time.time(), []]            
            }   
        
            self.data.append(data) 
            await asyncio.sleep( 1.0 / self.sample_rate )
            
