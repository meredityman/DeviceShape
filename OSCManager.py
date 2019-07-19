from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

class OSCComunication:
    target_ip = ""
    ping_num  = 0
    server = None
    client = None

    def __init__(self, host_ip, status, in_port = 3821):
        self.in_port = in_port
        self.status  = status
        self.host_ip = host_ip

        self.dispatcher = Dispatcher()
        
        self._setup_server()
    
    def close(self):
        print("Exit")
        self._send_exit()
    
    def update(self):
        server.handle_request()
        
        if(self.client == None):
            return
            
        self._ping()
        self._send_status()

    def send(self, address, args):
        if(self.client == None):
            return
            
        print(address)
        self.client(address, args)
            
    
    def _ping(self):
        print("Ping")
        self.send("/ping/", [ self.ping_num ])
        self.ping_num = self.ping_num + 1

    def _send_exit(self):
        self.send("/exit/", [ True ])
        
    def _send_status(self):
        print("Sending status")
        
        for key, value in self.status.items():
            address = "/status/" + key + "/"
            self.send(address, [ value ])
            
    def _setup_sender(self):
        print("Setting up client {}, {}".format(self.target_ip, self.out_port))
        self.client = SimpleUDPClient(self.target_ip, self.out_port)
        
    def _setup_server(self):
        print("Setting up server {}, {}".format(self.host_ip, self.in_port))

        self.server = BlockingOSCUDPServer((self.host_ip, self.in_port), dispatcher)
        
        dispatcher.map("/handshake/", self._handshake_handler) 
        dispatcher.map("/ping/"     , self._ping_handler )
        dispatcher.map("/start/"    , self._start_handler)
        dispatcher.map("/stop/"     , self._stop_handler )
        
                
    def _handshake_handler(self, address: str, *osc_arguments: List[Any]) -> None:
        if(self.target_ip != "") : return
        
        self.target_ip = info[0]
        self.out_port  = int(args[0])
        
        print("Handshake received. IP: {} PORT: {}".format(
            self.target_ip, 
            self.out_port  ))
            
        self._setup_sender()
            

    def _ping_handler(self, address: str, *osc_arguments: List[Any]) -> None:
        print("Ping received")
        pass
        
    def _start_handler(self, address: str, *osc_arguments: List[Any]) -> None:
        pass
        
    def _stop_handler(self, address: str, *osc_arguments: List[Any]) -> None:
        pass
