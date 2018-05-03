import socket
import sys
from server import Server

class Client():

    def __init__(self, addr, user):
        self.server = Server(addr)
        self.server.start()
        self.addr = addr 
        self.user = user

    def send(self):
        ip = input("ip: ")
        port = input("port: ")
        msg = input("msg: ")
        addr = (ip, int(port))
        self.server.sendTo(addr, msg, self.user)
        

    def connections(self):
        print(self.server.get_connections())

    def get_msgs(self):
        ip = input("ip: ")
        self.server.receiveFrom(ip)

    def shutdown(self):
        self.server.shutdown()