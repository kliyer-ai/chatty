from threading import Thread
import struct
import queue

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
        print("Connection from", self.addr)
        while not self.closed:
            self.flush_send()
            self.receive()
        self.c.close()


    def receive(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        raw_msg = self.recvall(msglen)
        self.received.put(str(raw_msg, 'utf-8')) 

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

    def send(self, msg):
        msg = bytes(msg, 'utf-8')
        msg = struct.pack('>I', len(msg)) + msg
        self.to_send.put(msg)

    def flush_send(self):
        while not self.to_send.empty():
            try:
                msg = self.to_send.get()
                self.c.sendall(msg)
            except:
                print("Could not deliver message to", self.addr)

    def shutdown(self):
        self.closed = True