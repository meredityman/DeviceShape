import os
import datetime
import asyncio

from src.OSCManager      import *
from src.AdcDataSource   import AdcDataSource
from src.PolarDataSource import PolarDataSource
from src.DataLogger      import LoggingManager
from src.Power           import Power
from src.Config          import GetConfig
from src.AudioRecorder   import AudioRecorder 
from src.Writer          import Writer

config_path = "device_config.csv"
data_path = "/media/data"


def main():
    global oscComunication, logging_manager, dataSources, power, audio, writer
    
    config = GetConfig(config_path)
    print(config)
    
    writer = Writer(data_path)
    
    power = Power()
    
    ## Setup OSC   
    oscComunication = OSCComunication(config["IP"])
    asyncio.ensure_future( oscComunication.start_server() )
    
    ## Setup Data Sources    
    dataSources = [
        AdcDataSource(),  
        PolarDataSource(config["PolarMAC"]),  
    ]
    
    audio = AudioRecorder(writer)
    
    
    ## Setup Logging
    logging_manager = LoggingManager(writer)    
    for dataSource in dataSources:
        logging_manager.add_logging_channel(dataSource.name)

    
    loop = asyncio.get_event_loop()    
    
    
    asyncio.ensure_future(main_loop())
    asyncio.ensure_future(audio.main_loop())
    asyncio.ensure_future(oscComunication.main_loop())
    
    for dataSource in dataSources:
        asyncio.ensure_future(dataSource.main_loop())
    
    try:    
        loop.run_forever()        
    except (KeyboardInterrupt, SystemExit):
        oscComunication.close()
        loop.close()

    print("End")


async def main_loop():
    global oscComunication, logging_manager, dataSources, power, audio, writer
        
        
    #await audio.startRecording(10)    
    
    while(True):
        
        for dataSource in dataSources:
            logging_manager.write_data_source(dataSource)
            
            
        oscComunication.queue_messages( power.get_status_mesages() )
        oscComunication.queue_messages( writer.get_status_mesages())
        
        await asyncio.sleep(1)



if __name__ == "__main__":
    main()
