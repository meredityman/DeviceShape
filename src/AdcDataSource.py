from src.ADCPi import ADCPi
import asyncio
from datetime import datetime

import RPi.GPIO as GPIO

from src.BaseDataSource import BaseDataSource

RIGHT_GPIO = 23
LEFT_GPIO  = 24


class AdcDataSource(BaseDataSource):

    bit_rates = {
    12 : 240,
    14 : 60,
    16 : 15,
    18 : 3.75
    }
    
    channels = [1, 2, 3, 4, 5, 6, 7, 8]


    def __init__(self, sample_rate = 10, address=0x68, address2=0x69, bit_rate=14):
        self.is_attached = False
        i2c_valid        = False
        self.adc_latest  = []
        GPIO.setup(RIGHT_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(LEFT_GPIO , GPIO.IN, pull_up_down = GPIO.PUD_UP)

        rDown = not GPIO.input(LEFT_GPIO)
        lDown = not GPIO.input(RIGHT_GPIO)
             
        

        if(rDown and lDown):
            print("ADC GPIO Error")
        elif(rDown):
            self.orientation = 'f'
            self.is_attached = True
        elif(lDown):
            self.orientation = 'b'
            self.is_attached = True

        if(self.is_attached):    
            try:    
                self.adc = ADCPi(address, address2, bit_rate)
                i2c_valid = True                
            except OSError:
                print("I2C not found at address")
            
        
        is_setup = self.is_attached and i2c_valid
        super(AdcDataSource, self).__init__("ADC", sample_rate, is_setup)

    def get_status_messages(self):
        return [
            ("/{}/connected/".format(self.name), self.is_setup),
            ("/{}/adc/".format(self.name), self.adc_latest)
        ]

    async def close(self):
        pass
    
    def validate_sample_rate(self, sample_rate, bit_rate):
        if bit_rate in self.bit_rates:
            max_sample_rate = self.bit_rates[bit_rate]
        else :
            print("bit rate {} not permitted".format(bit_rate))
            bit_rate = 16
            max_sample_rate = self.bit_rates[bit_rate]
        
        if(sample_rate > max_sample_rate):
            print("Requested sample rate too high")
            
        return min(max_sample_rate, sample_rate)
     

    async def loop_setup(self): 
        pass
     
    async def loop_work(self):
        if(self.is_setup):
            data = [self.orientation]
            for ch in self.channels:                
                try:
                    data.append( self.adc.read_raw(ch) )

                except TimeoutError:
                    pass
            
            
            #dstr = ""
            #for ch, val in data.items():
            #   dstr += "{} {}\t".format(ch, val[1])

            #print(dstr, end='\r')
            
            self.data.append({"ADC" : (datetime.now(), data) }) 
            self.adc_latest = data
