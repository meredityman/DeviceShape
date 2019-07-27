import asyncio
import time
import random


class Worker():
    
    def __init__(self, freq):
        self.freq = freq
        self.data = []


    async def work(self):
    
        while(True):
            print("loop at (" + str(self.freq) + ")")
            self.data.append(random.random())
            await asyncio.sleep(self.freq)



async def mainThread( workers):
    while True:
        await asyncio.sleep(1)
        print("Check")
        for worker in workers:
            if(len(worker.data) > 0):
            
                print("Worker " + str(worker.freq) + ":")
                print(worker.data)
                worker.data = []

async def main():
    loop = asyncio.get_event_loop()
    try:
        workers = [
            Worker(0.01),
            Worker(0.03)
        ]
        
        for worker in workers:
             asyncio.ensure_future(worker.work())
       
        asyncio.ensure_future(mainThread(workers))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
        
if __name__ == "__main__":
    asyncio.run(main())