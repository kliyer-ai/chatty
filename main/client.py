import socket
import sys
from server import Server

class Client():

    def __init__(self, addr, user):
        self.server = Server(addr, user)
        self.server.start()
        self.addr = addr 
        self.user = user

    def send(self):
        user = input("user: ")
        msg = input("msg: ")
        self.server.sendTo(user, msg)
        

    def pending(self):
        print(self.server.get_pending())

    def get_msgs(self):
        ip = input("user: ")
        msgs = self.server.receiveFrom(ip)
        for msg in msgs:
            print("Received on", msg["received"], "from", msg["sender"])
            print(msg["text"])

    def approve(self, user):
        self.server.pending[user].approved.set()

    def shutdown(self):
        self.server.shutdown()