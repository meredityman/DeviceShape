import asyncio
import random


class Thing():

    def __init__(self):
        self.data = []

    async def  start(self):

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(main_loop())

        
    async def main_loop(self):
    
        while(True):
            
            data = {}            
            for ch in range(10):                
                data[str(ch)] = random.random()
            
            print(data)
            self.data.append(data)
            
            await asyncio.sleep( random.random() * 2 )


async def main():
    global thing
    
    thing = Thing()
    
    await thing.start()    
    await main_loop()



async def main_loop():
    global thing

    while(True):
    
        print("Loop")
        
        if (len(thing.data) > 0):
            print (thing.data)
            thing.data  = []
        
    
        await asyncio.sleep( random.random() * 1 )

if __name__ == "__main__":
    asyncio.run(main())