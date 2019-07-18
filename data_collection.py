import os
import csv

from getmac import get_mac_address

def main():
    print("Hello world")
    
    with open('device_config.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
            
    ip_mac = get_mac_address(ip="192.168.0.1")
    
    print("My MAC Address is " + ip_mac)

if __name__ == "__main__":
    main()
