from threading import Thread
import struct
import json
import socket
import select

class Peer(Thread):
    
    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(5)

        self.connections = {}

    def run(self):
        pass

    def handle_accept(self):
        readable, _, _ = select.select([self.sock], [], [])
        c, addr = readable[0].accept()

    def listen(self):
        pass

    def sendTo(self):
        pass