from datetime import datetime 
import os 
import shutil

class Writer():
    min_space = 1e+9
    
    def __init__(self, path):
        self.path = path
    
        self.status       = {
             "valid"      : False,
             "total_space": None ,
             "used_space" : None ,
             "free_space" : None ,
             "remain_pct" : None 
        }
        
        self.check_remaining_space()
    
    def get_status_mesages(self):
        self.check_remaining_space()
         
        messages = []
        for (key, value) in self.status.items():
            messages.append(
                ("/writer/" + key + "/",
                value)
            )
            
        return messages
        
    def _valid(self):
        return self.status["valid"]
        
    def _valid_to_write(self):
        return self.status["valid"] and (self.status["free_space"] > self.min_space)
    
    
    def check_remaining_space(self):
        status = self.status

        status["valid"] = os.path.isdir(self.path)
    
        if(status["valid"]):
            total, used, free = shutil.disk_usage(self.path)
    
            status["total_space"] = float(total)
            status["used_space"]  = float(used)
            status["free_space"]  = float(free)
            status["remain_pct"]  = status["free_space"] / status["total_space"]
