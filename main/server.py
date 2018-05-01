import socket
from echoHandler import EchoHandler
from simpleHandler import SimpleHandler
from threading import Thread, Lock 

class Server(Thread):


    def __init__(self, addr):
        Thread.__init__(self)
        #Thread.daemon = True

        self.addr = addr

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(5)        

        self.connections = {}
        self.closed = False
        
        self.lock = Lock()

    def run(self):
        print("Sever runnin on", self.addr)

        while not self.closed:
            self.accept()

        self.sock.close()      
        print("Socket closed")

    def accept(self):
        c, addr = self.sock.accept()            
        #handler = EchoHandler(c, addr)
        handler = SimpleHandler(c, addr)
        handler.start()
        self.connections[addr[0]] = handler

    def sendTo(self, addr, msg):
        with self.lock:
            if addr[0] in self.connections:
                self.connections[addr[0]].send(msg)
            else:
                print("Could not find connection")

    def receiveFrom(self, ip):
        if ip in self.connections:
            msgs = self.connections[ip].get_msgs()
            for msg in msgs:
                print(msg)
        else:
            print("Could not find connection")     


    def shutdown(self):
        self.closed = True

    def get_connections(self):
        cs = []
        with self.lock:
            for c in self.connections.keys():
                cs.append(c)
        return c

