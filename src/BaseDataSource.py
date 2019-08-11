import asyncio
class BaseDataSource():
    

    def __init__(self, name, sample_rate, is_setup = False) :
        self.name = name
        self.data = []
        self.running = False;
        self.sample_rate = sample_rate
        
        self.is_setup = is_setup        
 
        if( self.is_setup ):
            print("{} Initialised".format(self.name))
        else:
            print("{} Not Initialised".format(self.name))
        
    def clear_cache(self):
        self.data = []
        
    def get_data(self, clear_cache=False):
        if(clear_cache):
            data = self.data
            self.clear_cache()
            return data
        else:    
            return self.data
            
    def get_status_messages(self):
       return [("/{}/connected/".format(self.name), self.is_setup)]
            
    async def loop_setup(self):
        raise NotImplementedError()
        
    async def loop_work(self):
        raise NotImplementedError() 
        
                
    async def close(self):
        raise NotImplementedError() 
            
    async def main_loop(self):
    
        await self.loop_setup()
        self.running = True 
        while(self.running):
            try:
                await self.loop_work() 

                await asyncio.sleep( 1.0 / self.sample_rate )
            except (KeyboardInterrupt, SystemExit):
                raise
            
