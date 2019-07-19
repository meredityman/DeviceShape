import os
import csv
import shutil
from getmac import get_mac_address
from OSCManager  import *
import time

data_path = "/media/data"

def main():
    print("Hello world")
    
    with open('device_config.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
            
    wlan_mac = get_mac_address(interface="wlan0")
    
    print("My MAC Address is " + wlan_mac)
    
    print(os.stat(data_path))
    
    total, used, free = shutil.disk_usage(data_path)

    print("Total: %d GB" % (total // (2**30)))
    print("Used: %d GB" % (used // (2**30)))
    print("Free: %d GB" % (free // (2**30)))
    
    
    oscComunication = OSCComunication()

    while(True):
        time.sleep(1)
        print("Here")
        oscComunication.update()

    print("End")

def setup():
    pass

def loop():
    pass
    
    

if __name__ == "__main__":
    main()
