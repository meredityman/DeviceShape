import csv
from getmac import get_mac_address

def GetConfig(config_path):
    wlan_mac = get_mac_address(interface="wlan0")
    wlan_mac = wlan_mac.upper().replace(':', '-')

    field_names = [
        "ID",
        "Color",
        "MAC Address",
        "IP",
        "PolarMAC"]
    
    with open(config_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:

            for field in field_names:
                if(field not in row.keys()):
                    raise Exception("Row does not contain expected field " + field)

            if( row["MAC Address"].casefold() == wlan_mac.casefold()):
                return row
    
    raise Exception("Entry for this device not found") 