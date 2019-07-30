import os
import time
import shutil



class LoggingManager():
    min_space = 1e+9

    def __init__(self, path):
        self.logging_channels = {}
        self.path = path
        
        self.status           = {
             "valid"      : False,
             "total_space": None ,
             "used_space" : None ,
             "free_space" : None ,
             "remain_pct" : None 
        }
        
        self.check_remaining_space()

       
    def add_logging_channel(self, name):
    
        new_logging_channel = LoggingChannel(name, self.path)
        self.logging_channels[name] = new_logging_channel
        
    def check_remaining_space(self):
        status = self.status
    
        status["valid"] = os.path.isdir(self.path)
            
        total, used, free = shutil.disk_usage(self.path)
    
        status["total_space"] = float(total)
        status["used_space"]  = float(used)
        status["free_space"]  = float(free)
        status["remain_pct"]  = status["free_space"] / status["total_space"]

    def _valid(self):
        return self.status["valid"]
        
    def _valid_to_write(self):
        return self.status["valid"] and (self.status["free_space"] > self.min_space)
    
    
    def write_data_source(self, dataSource):
        name = dataSource.name
        data = dataSource.get_data();
        
        if(len(data) == 0 ) : return
        
        for d in data:
            for key, values in d.items():
                self.write_entry(name, key, values[0], values[1])
            
    
    def write_entry(self, name, type, time, *values):
        
        if(not self._valid_to_write() ):
            print("Volume not valid for writing")
            return
            
        if(name not in self.logging_channels):
            print( "Logging for " + name + " not setup")
            return

        self.logging_channels[name].write_entry(type, time, values)
    
class LoggingChannel():
    file_period = 1200

    def __init__(self, name, path):
        self.name = name
        
        
        self.path = os.path.join(path, name)
        os.makedirs(self.path, exist_ok = True)

        self.log_file = None
        self._open_new_file()
     
    def __del__(self):
        if(self.log_file is not None):
            self.log_file.close()
     
    def write_entry(self, type, dtime, *values):
        self._open_new_file_iff()
        
        line = ""
        line += time.strftime("%Y%m%d-%H%M%S", dtime)
        line += ", "
        line += type
        line += ", "
        line += ', '.join(map(str, values)) 
        line += "\n"
        
        self.log_file.write(line)
    
    def _open_new_file_iff(self):
        if( (time.time() - time.mktime(self.start_file_time)) > self.file_period):
            self._open_new_file()
        
    def _open_new_file(self):

        if(self.log_file is not None):
            self.log_file.close
            
        self.start_file_time = time.localtime()
            
        file_name = self.name + "_" + time.strftime("%Y%m%d-%H%M%S", self.start_file_time) + ".txt"
        
        path_path = os.path.join(self.path, file_name)
        
        self.log_file = open(path_path, "a")
        
