import socket
from echoHandler import EchoHandler

class Server():

    peers = []
    connections = []

    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(1)
        self.addr = addr

    def listen(self):
        print("listening...")
        while True:
            c, addr = self.sock.accept()            
            eh = EchoHandler(c, addr)
            eh.start()
            self.connections.append(eh)


        #self.connections.append(c)
        #print(data)
