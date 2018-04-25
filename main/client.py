import socket
import sys

class Client():

    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        self.addr = addr

    def send(self):
        while True:
            data = input("say something: ")
            self.sock.sendall(bytes(data, "utf-8"))
            data = self.sock.recv(1024)
            print("server says:", str(data, "utf-8"))