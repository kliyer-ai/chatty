from threading import Thread

class EchoHandler(Thread):

    def __init__(self, c, addr):
        Thread.__init__(self)
        Thread.daemon = True
        self.c = c
        self.addr = addr
        print("connection from", addr)
        

    def run(self):
        while True:
            data = self.c.recv(1024)
            self.c.sendall(data)