from datetime import datetime 
import os 
import shutil

class Writer():
    min_space = 1e+9
    
    def __init__(self, path, config):
        self.path = path
    
        self.status       = {
             "valid"      : False,
             "total_space": None ,
             "used_space" : None ,
             "free_space" : None ,
             "remain_pct" : None 
        }
        
        self.check_remaining_space()
        
        self._write_device_details(config)
    
    def _write_device_details(self, config):
        filePath = os.path.join(self.path, "device.txt")
    
        with open(filePath, 'w') as f:
            for key, value in config.items():
                f.write("{}\t{}\n".format(key, value))
    
    
    def get_status_messages(self):
        self.check_remaining_space()
         
        messages = []
        for (key, value) in self.status.items():
            if(value is not None):
                messages.append(("/writer/{}/".format(key),value))
            
        return messages
        
    def _valid(self):
        return self.status["valid"]
        
    def _valid_to_write(self):
        return self.status["valid"] and (self.status["free_space"] > self.min_space)
    
    
    def check_remaining_space(self):
        status = self.status

        status["valid"] = os.access(self.path, os.W_OK)
    
        if(status["valid"]):
            total, used, free = shutil.disk_usage(self.path)
    
            status["total_space"] = float(total)
            status["used_space"]  = float(used)
            status["free_space"]  = float(free)
            status["remain_pct"]  = status["free_space"] / status["total_space"]
