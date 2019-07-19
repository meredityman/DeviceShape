from osc4py3.as_comthreads import *
from osc4py3.oscmethod    import *
from osc4py3 import oscbuildparse
import time

class OSCComunication:
    target_ip = ""

    def __init__(self, host_ip, status, in_port = 3821):
        self.in_port = in_port
        self.status  = status
        self.host_ip = host_ip

        osc_startup()
        self._setup_receiver()
    
    def __del__(self):
        osc_terminate()
    
    def update(self):
        osc_process()
        
        if(self.target_ip == ""):
            return
        else:
            self._ping()
            self._send_status()

    def send(self, msg):
        if(self.target_ip != ""):
            osc_send(msg, "sender")
            
    
    def _ping(self):
        print("Ping")
        msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        self.send(msg)
        
    def _send_status(self):
        
        messages = []
        for key, value in status.items():
            address = "/status/" + key
            msg = oscbuildparse.OSCMessage("address", None, [ value ]) 
            messages.append(msg)
            
        exectime = time.time()
            
        bun = oscbuildparse.OSCBundle(oscbuildparse.unixtime2timetag(exectime), messages)
        
        send(bun)
            
    def _setup_sender(self):
        print("Setting up sender {}, {}".format(self.target_ip, self.out_port))
        osc_udp_client(self.target_ip, self.out_port , "sender")
        
    def _setup_receiver(self):
        print("Setting up receiver")

        osc_udp_server(self.host_ip, self.in_port , "receiver") # Receiver
        
        osc_method(
            "/*/",
            self._all_message_handler,
            argscheme = OSCARG_ADDRESS )
           
        
        osc_method(
            "/handshake/",
            self._handshake_handler,
            argscheme = OSCARG_SRCIDENT + OSCARG_DATAUNPACK )
           
           
        osc_method("/ping/"      , self._ping_handler )
        osc_method("/start/"      , self._start_handler)
        osc_method("/stop/"       , self._stop_handler )
        
    def _all_message_handler(self, adr):
        #print(adr)
        pass
                
    def _handshake_handler(self, info, *args):
        if(self.target_ip != "") : return
        
        self.target_ip = info[0]
        self.out_port  = int(args[0])
        
        print("Handshake received. IP: {} PORT: {}".format(
            self.target_ip, 
            self.out_port  ))
            
        self._setup_sender()
            

    def _ping_handler(self, *args):
        print("Ping received")
        pass
        
    def _start_handler(self, *args):
        pass
        
    def _stop_handler(self, *args):
        pass
