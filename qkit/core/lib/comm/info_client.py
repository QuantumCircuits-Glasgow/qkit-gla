import sys
import zmq
from signals import SIGNALS

RSIGNALS = dict((v,k) for k,v in SIGNALS.iteritems())
from qkit.config.environment import cfg



class info_client(object):
    def __init__(self,host = None, port = None):
        
        if host:
            self.host = host
        else:
            self.host = cfg.get('info_host','localhost')
        if port:
            self.port = port
        else:
            self.port = cfg.get('info_port',5600)
            
        self.start_client(self.port,self.host)
        
    def start_client(self,port,host):
        print port, host
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        self.socket.connect ("tcp://%s:%s" %(host, port))
    def listen_to(self,topic):
        "hook up to topic (defined in signals.py)"
        if SIGNALS.has_key(topic):
                sig = SIGNALS.get(topic)
                self.socket.setsockopt(zmq.SUBSCRIBE, str(sig).encode())
    def listen_to_all(self):
        for topic in SIGNALS.keys():
            self.listen_to(topic)
            
    def get_message(self,readable_topic = False):
        "wait until a message is available and return it"
        tid,message =self.socket.recv().split(":",1)
        if readable_topic:
            return RSIGNALS.get(int(tid)), message
        else:
            return tid, message
        
    def print_message(self):
        "wait until a message is available and print it"
        #tid,message =self.socket.recv().split(":",1)
        #print RSIGNALS.get(int(tid)),":", message
        print self.get_message(readable_topic = True)
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        host =  int(sys.argv[1])
        port =  int(sys.argv[2])
        ifc = info_client(host,port)
    else:
        ifc = info_client()
    ifc.listen_to_all()
    for i in range(10):
        ifc.print_message()
