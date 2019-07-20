from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
import asyncio

class OSCComunication:
    target_ip = ""
    ping_num  = 0
    server = None
    client = None

    def __init__(self, host_ip, status, in_port = 3821):
        self.in_port = in_port
        self.status  = status
        self.host_ip = host_ip
       
        self._setup_server()
    
    def close(self):
        self._send_exit()
        
        self.transport.close()
    
    def update(self):
        print("loop")

        if(self.client == None):
            return
            
        self._send_ping()
        self._send_status()

    def send(self, address, args):
        if(self.client == None):
            return
            
        print(address)
        print(args)
        self.client.send_message(address, args)
            
    
    def _send_ping(self):
        self.send("/ping/", [ self.ping_num ])
        self.ping_num = self.ping_num + 1

    def _send_exit(self):
        self.send("/exit/", [ True ])
        
    def _send_status(self):
        print("Sending status")
        
        for key, value in self.status.items():
            address = "/status/" + key
            self.send(address, value)
            
    def _setup_sender(self):
        print("Setting up client {}, {}".format(self.target_ip, self.out_port))
        self.client = SimpleUDPClient(self.target_ip, self.out_port)
        
    def _setup_server(self):
        print("Setting up server {}, {}".format(self.host_ip, self.in_port))

        self.dispatcher = Dispatcher()
        
        self.dispatcher.map("/handshake/", self._handshake_handler) 
        self.dispatcher.map("/ping/"     , self._ping_handler )
        self.dispatcher.map("/start/"    , self._start_handler)
        self.dispatcher.map("/stop/"     , self._stop_handler )
        
        self.server = AsyncIOOSCUDPServer((self.host_ip, self.in_port), self.dispatcher, asyncio.get_event_loop())
        
    async def start(self):
        self.transport, self.protocol = await self.server.create_serve_endpoint()  # Create datagram endpoint and start serving

        
                
    def _handshake_handler(self, address, osc_arguments):
        if(self.target_ip != "") : return
        
        self.target_ip = "192.168.0.199"
        self.out_port  = osc_arguments
        
        print("Handshake received. IP: {} PORT: {}".format(
            self.target_ip, 
            self.out_port  ))
        
        self.dispatcher.unmap("/handshake/", self._handshake_handler)
        self._setup_sender()
            

    def _ping_handler(self, address, osc_arguments):
        print("Ping received")
        pass
        
    def _start_handler(self, address, osc_arguments):
        pass
        
    def _stop_handler(self, address, osc_arguments):
        pass
