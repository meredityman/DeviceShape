import os
from datetime import datetime
import asyncio

from src.OSCManager      import *
from src.AdcDataSource   import AdcDataSource
from src.PolarDataSource import PolarDataSource
from src.DataLogger      import LoggingManager
from src.Power           import Power
from src.Config          import GetConfig
from src.AudioRecorder   import AudioRecorder 
from src.Writer          import Writer

config_path = data_path = os.path.join( os.path.dirname(__file__), "device_config.csv")
data_path = "/media/data"


def main():
    global oscComunication, logging_manager, dataSources, power, audio, writer
    
    print("---------------------------------------------")
    print("Starting Program [{}]".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    print("---------------------------------------------")
    
    config = GetConfig(config_path)
    
    for key, value in config.items():
        print("{}\t\t{}".format(key, value))
    print("---------------------------------------------")
    
    writer = Writer(data_path, config)
    
    power = Power()
    
    ## Setup OSC   
    oscComunication = OSCComunication(config["IP"])
    asyncio.ensure_future( oscComunication.start_server() )
    
    ## Setup Data Sources    
    dataSources = [
        AdcDataSource(),  
        PolarDataSource(config["PolarMAC"])  
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
        dataSource.start()
    
    loop.run_forever()
    
    print("---------------------------------------------")
    print("Ending Program [{}]".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    print("---------------------------------------------")


async def main_loop():
    global oscComunication, logging_manager, dataSources, power, audio, writer
    print("---------------------------------------------")
    print("Starting main loop")
    print("---------------------------------------------")

    running = True
    while(running):
        try:
            for dataSource in dataSources:
                logging_manager.write_data_source(dataSource)
                oscComunication.queue_messages( dataSource.get_status_messages() )
                
                
            oscComunication.queue_messages( power.get_status_messages() )
            oscComunication.queue_messages( writer.get_status_messages())
            oscComunication.queue_messages( audio.get_status_messages())
            
            await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            for dataSource in dataSources:
                await dataSource.close()
        
            oscComunication.close()
            running = False



if __name__ == "__main__":
    main()
