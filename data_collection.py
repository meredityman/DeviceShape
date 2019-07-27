import os
import time
import asyncio

from src.OSCManager      import *
from src.AdcDataSource   import AdcDataSource
from src.PolarDataSource import PolarDataSource
from src.DataLogger      import LoggingManager
from src.Power           import Power
from src.Config          import GetConfig

config_path = "device_config.csv"
data_path = "/media/data"


def main():
    global oscComunication, logging_manager, dataSources, power
    
    config = GetConfig(config_path)
    print(config)
    
    power = Power()
    
    ## Setup OSC   
    oscComunication = OSCComunication(config["IP"])
    asyncio.ensure_future( oscComunication.start_server() )
    
    ## Setup Data Sources    
    dataSources = [
        AdcDataSource(),  
        PolarDataSource(config["PolarMAC"]),  
    ]
    
    
    ## Setup Logging
    logging_manager = LoggingManager(data_path)    
    for dataSource in dataSources:
        logging_manager.add_logging_channel(dataSource.name)

    
    loop = asyncio.get_event_loop()    
    
    asyncio.ensure_future(main_loop())
    for dataSource in dataSources:
        asyncio.ensure_future(dataSource.main_loop())
    
    
    try:    
        loop.run_forever()        
    except (KeyboardInterrupt, SystemExit):
        loop.close()
        oscComunication.close()

    
    print("End")



async def main_loop():
    global oscComunication, logging_manager, dataSources, power
    
    while(True):
        print("Loop")
        if( power.is_low_power()) : print("Low Power!!")
    
        oscComunication.update()
        
        for dataSource in dataSources:
            logging_manager.write_data_source(dataSource)
        
        await asyncio.sleep(1)



if __name__ == "__main__":
    main()
