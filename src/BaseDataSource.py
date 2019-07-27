import asyncio
import time.time()

class BaseDataSource():

    def __init__(self, name, sample_rate) :
        self.name = name
        self.data = []
        self.running = False;
        print("{} Setup".format(self.name))
        
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
            
