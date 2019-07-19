import os
import csv
import shutil
from getmac import get_mac_address
from OSCManager  import *
import time

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
        
        
        
        #for field in field_names:
        #    if(field not in reader.keys()):
        #        raise Exception("CSV does not contain " + field) 
        
        for row in reader:
            print(row.keys())

            print(row["MAC Address"])
            for field in field_names:
                if(field not in row.keys()):
                    raise Exception("Row does not contain expected feild " + field)

            if( row["MAC Address"].casefold() == wlan_mac.casefold()):
                return row
    
    raise Exception("Entry for this device not found") 

def main():
    print("Hello world")
    
    config_data = get_config_data()

    #print(os.stat(data_path))
    
    #total, used, free = shutil.disk_usage(data_path)
    #
    #print("Total: %d GB" % (total // (2**30)))
    #print("Used: %d GB" % (used // (2**30)))
    #print("Free: %d GB" % (free // (2**30)))
    
    
    oscComunication = OSCComunication(config_data["IP"])

    #while(True):
    #    time.sleep(1)
    #    print("Here")
    #    oscComunication.update()
    #
    #print("End")

def setup():
    pass

def loop():
    pass
    
    

if __name__ == "__main__":
    main()
