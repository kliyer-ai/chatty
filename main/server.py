import socket
from echoHandler import EchoHandler
from simpleHandler import SimpleHandler
from threading import Thread, Lock 
from connector import Connector
from approver import Approver

class Server(Thread):


    def __init__(self, addr, sender):
        Thread.__init__(self)
        Thread.daemon = True

        self.addr = addr
        self.sender = sender

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(5)        

        self.pending = {}
        self.closed = False

        self.unread = {}
        self.users = {}
        
        self.lock = Lock()

    def run(self):
        print("Sever runnin on", self.addr)

        while not self.closed:
            self.accept()

        self.sock.close()      
        print("Socket closed")

    def accept(self):
        c, addr = self.sock.accept()            
        app = Approver(self, c)
        app.start()
        

    def sendTo(self, recipient, msg):
        with self.lock:
            if recipient in self.users:
                self.users[recipient].send(msg)
            else:
                ip = input("ip: ")
                port = input("port: ")
                addr = (ip, int(port))

                try:
                    c = socket.create_connection(addr)
                    con = Connector(self, c, msg)
                    con.start()
                    self.pending[addr[0]] = con
                except:
                    print("Cannot connect to given address")

    def receiveFrom(self, user):
        with self.lock:

            if user in self.users:
                msgs = self.users[user].get_msgs()
                return msgs
            else:
                return []

    def add_unread(self, msg):
        with self.lock:
            user = msg["name"]
            if user in self.unread:
                self.unread[user].append(msg)
            else:
                self.unread[user] = [msg]


    def shutdown(self):
        self.closed = True

    def get_pending(self):
        cs = []
        with self.lock:
            for c in self.pending.keys():
                cs.append(c)
        return cs

