from osc4py3.as_comthreads import *
from osc4py3.oscmethod    import *
from osc4py3 import oscbuildparse
import socket 
import logging


class OSCComunication:
    target_ip = ""

    def __init__(self, host_ip, in_port = 3821 ):
        self.in_port = in_port
        self.host_ip = host_ip
        


        #osc_startup()

        logging.basicConfig(format='%(asctime)s - %(threadName)s ø %(name)s - '
'%(levelname)s - %(message)s')
        logger = logging.getLogger("osc")
        logger.setLevel(logging.DEBUG)
        osc_startup(logger=logger)

        if( self.host_ip is not None) : 
            self._setup_receiver()



    
    def __del__(self):
        osc_terminate()
    
    def update(self):
        osc_process()
        
        if(self.target_ip == ""):
            return
        else:
            self.ping()

    def send(self, msg):
        if(self.target_ip != ""):
            osc_send(msg, "sender")
            
    
    def ping(self):
        print("Ping")
        msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        self.send(msg)
        
        
    def report_status(self):
        pass
        #msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
        #osc_send(msg, "sender")
            
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
        print("Ping recieved")

        pass
        
    def _start_handler(self, *args):
        pass
        
    def _stop_handler(self, *args):
        pass
