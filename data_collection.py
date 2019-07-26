import os
import csv
from getmac import get_mac_address
import time
import random
import asyncio

from src.OSCManager  import *
from src.AdcDataSource   import AdcDataSource

config_path = "device_config.csv"

def get_config_data():
    wlan_mac = get_mac_address(interface="wlan0")
    wlan_mac = wlan_mac.upper().replace(':', '-')


    print(wlan_mac)
    field_names = [
        "ID",
        "Color",
        "MAC Address",
        "IP"]
    
    with open(config_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            print(row.keys())

            print(row["MAC Address"])
            for field in field_names:
                if(field not in row.keys()):
                    raise Exception("Row does not contain expected field " + field)

            if( row["MAC Address"].casefold() == wlan_mac.casefold()):
                return row
    
    raise Exception("Entry for this device not found") 


async def main():
    global status, oscComunication
    
    config_data = get_config_data()
    
    oscComunication = OSCComunication(config_data["IP"])
    
    adcSource = AdcDataSource()
    await adcSource.start();
    
    await oscComunication.start_server()
    await main_loop()
    
    oscComunication.close()
    
    print("End")
 

async def main_loop():
    global status, oscComunication
    print("Starting main loop")
    try:
        while(True):
            oscComunication.update()
            await asyncio.sleep(0)

    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())
