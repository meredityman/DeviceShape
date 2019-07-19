from osc4py3.as_eventloop import *
from osc4py3.oscmethod    import *
from osc4py3 import oscbuildparse

import time

def ping(self):
    msg = oscbuildparse.OSCMessage("/ping/", None, [ True ])
    osc_send(msg, "sender")
    
osc_startup()

osc_udp_client("192.168.0.199", 4880 , "sender") # Receiver


print("In Loop")
while(True):
    time.sleep(1)
    ping()
    osc_process()