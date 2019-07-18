import os
import csv

def main():
    print("Hello world")
    
    with open('device_config.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

if __name__ == "__main__":
    main()
