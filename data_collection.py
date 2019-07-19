import os
import csv
import shutil
from getmac import get_mac_address
from OSCManager  import *
import time
import random

config_path = "device_config.csv"
data_path = "/media/data"


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

def update_status(status):
    #print(os.stat(data_path))
    
    total, used, free = shutil.disk_usage(data_path)
    
    status["total"]  = total
    status["used"]   = used
    status["free"]   = free
    status["random"] = random.random()

def main():
    print("Hello world")
    
    config_data = get_config_data()

    status = {}
    update_status(status);
    oscComunication = OSCComunication(config_data["IP"], status)

    i = 0
    while(i < 1000):
        i = i + 1
        #time.sleep(1)
        update_status(status);
        oscComunication.update()

    oscComunication.close()
    print("End")

def setup():
    pass

def loop():
    pass
    
    

if __name__ == "__main__":
    main()
