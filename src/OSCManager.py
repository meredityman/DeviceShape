from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
import asyncio

class OSCComunication:
    target_ip = ""
    ping_num  = 0
    ping_rate = 2
    server = None
    client = None

    def __init__(self, host_ip, in_port = 3821):
        self.in_port = in_port
        self.host_ip = host_ip
        self.running = False
        self.message_queue = []
        
        self._setup_server()
    
    def close(self):
        self._send_exit()
        self.transport.close()
        
    def queue_messages(self, msgs):
        for (address, msg) in msgs:
            self.queue_message(address, msg)
        
    def queue_message(self, address, msg):
        print(address)
        if(self.client != None):
            self.message_queue.insert(0, (address, msg))

    async def send_queue(self):
        for (address, msg) in self.message_queue:
            self.send(address, msg)
            asyncio.sleep(0)
            
        self.message_queue = []

    async def main_loop(self):
        self.running = True
        
        asyncio.ensure_future(self.ping_loop())
        
        while(self.running):
            await self.send_queue()
            await asyncio.sleep(0)
    
    async def ping_loop(self):
        while(True):
            if(self.client != None):
                self._send_ping()
                
            await asyncio.sleep(self.ping_rate)

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
        
    async def start_server(self):
        self.transport, self.protocol = await self.server.create_serve_endpoint()  # Create datagram endpoint and start serving
        return
        
                
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
