import os
import csv

from getmac import get_mac_address

def main():
    print("Hello world")
    
    with open('device_config.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
            
    wlan_mac = get_mac_address(interface="wlan0")
    
    print("My MAC Address is " + wlan_mac)

if __name__ == "__main__":
    main()
