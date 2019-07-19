from osc4py3.as_comthreads import *
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

    def __init__(self, in_port = 3821 ):
        self.in_port = in_port
        osc_startup()

        self.host_ip = get_host_name_IP()
        if( self.host_ip is not None) : 
            self._setup_receiver()


    
    def __del__(self):
        osc_terminate()
    
    def update(self):
        osc_process()

    def send(self, msg):
        if(found_master):
            osc_send(msg, "server")
            
    
    def ping(self):
        msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        self.send(msg)
        
    def report_status(self):
        pass
        #msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        #osc_send(msg, "sender")
            
    def _setup_sender(self):
        osc_udp_server(self.target_ip, self.out_port, "server")
        
    def _setup_receiver(self):
        print("Setting up receiver")

        osc_udp_server(self.host_ip, self.in_port , "receiver") # Reciver
        
        osc_method(
            "/*",
            self._all_message_handler,
            argscheme = OSCARG_ADDRESS )
           
        
        osc_method(
            "/handshake/",
            self._handshake_handler,
            argscheme = OSCARG_SRCIDENT + OSCARG_DATAUNPACK )
           
           
        osc_method( "/ping/"      , self._ping_handler )
        osc_method("/start/"      , self._start_handler)
        osc_method("/stop/"       , self._stop_handler )
        
    def _all_message_handler(self, adr):
        print(adr)
        pass
                
    def _handshake_handler(self, info, *args):
        print(info)
        pass
        
    def _ping_handler(self, *args):
        pass
        
    def _start_handler(self, *args):
        pass
        
    def _stop_handler(self, *args):
        pass
