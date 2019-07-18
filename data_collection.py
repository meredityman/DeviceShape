import os
import csv
import shutil


from getmac import get_mac_address

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

    
    

if __name__ == "__main__":
    main()
