from osc4py3.as_comthreads import *
from osc4py3.oscmethod    import *
from osc4py3 import oscbuildparse
import time

class OSCComunication:
    target_ip = ""
    ping_num  = 0

    def __init__(self, host_ip, status, in_port = 3821):
        self.in_port = in_port
        self.status  = status
        self.host_ip = host_ip

        osc_startup()
        self._setup_receiver()
    
    def close(self):
        print("Exit")
        self._send_exit()
        osc_process()
        time.sleep(3)
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
            print(msg)
            osc_send(msg, "sender")
            
    
    def _ping(self):
        print("Ping")
        msg = oscbuildparse.OSCMessage("/ping/", None, [ self.ping_num ])
        self.send(msg)
        self.ping_num = self.ping_num + 1

    def _send_exit(self):
        msg = oscbuildparse.OSCMessage("/exit/", None, [ True ])
        self.send(msg)
        
    def _send_status(self):
        print("Sending status")
        
        messages = []
        for key, value in self.status.items():
            address = "/status/" + key + "/"
            print(address + ": " + str(value))
            msg = oscbuildparse.OSCMessage(address, None, [ value ]) 
            #self.send(msg)
            messages.append(msg)

        bundle = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY, messages)
        self.send(bundle)
            
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
