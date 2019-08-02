from datetime import datetime 
import os 

from src.Writer import Writer

class LoggingManager():

    def __init__(self, writer):
        self.logging_channels = {}
        self.writer = writer

    def add_logging_channel(self, name):
    
        new_logging_channel = LoggingChannel(name, self.writer)
        self.logging_channels[name] = new_logging_channel
        
    def write_data_source(self, dataSource):
    
        if(not self.writer._valid_to_write() ):
            print("Volume not valid for writing")
            return
  
        name = dataSource.name
        data = dataSource.get_data();
        
        if(len(data) == 0 ) : return
        
        for d in data:
            for key, values in d.items():
                self.write_entry(name, key, values[0], values[1])       
    
    def write_entry(self, name, type, time, *values):
                   
        if(name not in self.logging_channels):
            print( "Logging for " + name + " not setup")
            return

        self.logging_channels[name].write_entry(type, time, values)
    
class LoggingChannel():
    file_period = 1200

    def __init__(self, name, writer):
        self.name = name
        self.writer = writer


        if(not self.writer._valid_to_write() ):
            print("Volume not valid for writing")
            return

        
        self.path = os.path.join(self.writer.path, name)
        os.makedirs(self.path, exist_ok = True)

        self.log_file = None
        self._open_new_file()
     
    def __del__(self):
        if(self.log_file is not None):
            self.log_file.close()
     
    def write_entry(self, type, dtime, *values):
        self._open_new_file_iff()
        
        line = ""
        line += datetime.strftime("%Y%m%d-%H%M%S-%f", dtime)
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

        if(not self.writer._valid_to_write() ):
            print("Volume not valid for writing")
            return

        if(self.log_file is not None):
            self.log_file.close
            
        self.start_file_time = datetime.now()
            
        file_name = self.name + "_" + self.start_file_time.strftime("%Y%m%d-%H%M%S") + ".txt"
        
        path_path = os.path.join(self.path, file_name)
        
        self.log_file = open(path_path, "a")
        
