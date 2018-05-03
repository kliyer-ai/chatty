from threading import Thread
import struct
import queue
import select
import json
from time import gmtime, strftime

class SimpleHandler(Thread):

    def __init__(self, c, addr):
        Thread.__init__(self)
        Thread.daemon = True
        self.c = c
        self.addr = addr

        self.received = queue.Queue()
        self.to_send = queue.Queue()

        self.closed = False
        

    def run(self):
        while not self.closed:
            self.flush_send()
            self.receive()
        self.c.close()


    def receive(self):
        c, _, _ = select.select([self.c], [], [], 1.)
        if c:
            # Read message length and unpack it into an integer
            raw_msglen = self.recvall(4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('>I', raw_msglen)[0]
            # Read the message data
            raw_msg = self.recvall(msglen)
            msg = str(raw_msg, 'utf-8')
            msg = json.loads(msg)
            msg["received"] = self.get_time()
            self.received.put(msg) 

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.c.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def get_msgs(self):
        msgs = []
        while not self.received.empty():
            msgs.append(self.received.get())
        return msgs

    def send(self, msg, user):
        msg = {
            "text" : msg,
            "sent" : None,
            "received": None,
            "sender" : user,
        }
        self.to_send.put(msg)

    def flush_send(self):
        while not self.to_send.empty():
            try:
                msg = self.to_send.get()
                msg["sent"] = self.get_time()
                msg = json.dumps(msg)
                msg = bytes(msg, 'utf-8')
                msg = struct.pack('>I', len(msg)) + msg
                self.c.sendall(msg)
            except:
                print("Could not deliver message to", self.addr)

    def get_time(self):
        return strftime("%d, %m, %Y %H:%M:%S", gmtime())

    def shutdown(self):
        self.closed = True