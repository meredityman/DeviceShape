import RPi.GPIO as GPIO

class Power():
    LOW_VOLTAGE_GPIO = 16
    def __init__(self) :
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LOW_VOLTAGE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        self.is_low_power()
    
    def get_status_messages(self):
        return [("/power/low/", self.is_low_power())]    
    
    def is_low_power(self):
        self.low_power = GPIO.input(self.LOW_VOLTAGE_GPIO)
        return self.low_power
    
    
