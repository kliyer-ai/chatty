import socket
from echoHandler import EchoHandler
from threading import Thread 

class Server(Thread):


    def __init__(self, addr):
        Thread.__init__(self)
        #Thread.daemon = True

        self.addr = addr

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(5)        

        self.connections = []
        self.closed = False

    def run(self):
        while not self.closed:
            print("adf")
            self.listen()

        self.sock.close()      

    def listen(self):
        c, addr = self.sock.accept()            
        eh = EchoHandler(c, addr)
        eh.start()
        self.connections[addr[0]] = eh


    def shutdown(self):
        self.closed = True
