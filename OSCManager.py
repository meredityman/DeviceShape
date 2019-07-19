from osc4py3.as_allthreads import *
from osc4py3.oscmethod    import *
from osc4py3 import oscbuildparse
import socket 

def get_host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
        
        return host_ip
    except: 
        print("Unable to get Hostname and IP") 


class OSCComunication:
    target_ip = ""

    def __init__(
        in_port     = 3821, 
        out_port    = 2881
    ):
        self.in_port  = in_port
        self.out_port = out_port
        
        osc_startup()  
        if( host_ip = get_host_name_IP() ) : 
                  
            _setup_receiver()
    

    def send(self, msg):
        if(found_master):
            osc_send(msg, "sender")
            
    
    def ping(self):
        msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        self.send(msg)
        
    def report_status(self):
        pass
        #msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        #osc_send(msg, "sender")
            
    def _setup_receiver(self):
        osc_udp_server(self.target_ip, self.out_port, "aservername")
        
    def _setup_sender(self):
        osc_udp_server(get_Host_name_IP(), self.in_port , "receiver") # Reciver
        
        osc_method("/handshake/"  , self._handshake_handler )
        osc_method("/ping/"       , self._ping_handler )
        osc_method("/start/"      , self._start_handler)
        osc_method("/stop/"       , self._stop_handler )
        
    def _handshake_handler(self, *args):
        print("Handshake")
        pass
        
    def _ping_handler(self, *args):
        pass
        
    def _start_handler(self, *args):
        pass
        
    def _stop_handler(self, *args):
        pass