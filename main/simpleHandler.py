from threading import Thread
import struct
import queue
import select
import json
from time import gmtime, strftime
import utils

class SimpleHandler(Thread):

    def __init__(self, server, c):
        Thread.__init__(self)
        Thread.daemon = True
        self.c = c
        self.server = server

        self.received = queue.Queue()
        self.to_send = queue.Queue()

        self.closed = False
        self.first_rcv = True
        

    def run(self):
        while not self.closed:
            self.flush_send()
            self.receive()
        self.c.close()


    def receive(self):
        c, _, _ = select.select([self.c], [], [], 1.)
        if c:
            msg = utils.recv_msg(self.c)
            msg = json.loads(msg)
            msg["received"] = utils.get_time()
            self.received.put(msg) 


    def get_msgs(self):
        msgs = []
        while not self.received.empty():
            msgs.append(self.received.get())
        return msgs

    def send(self, msg):
        msg = {
            "text" : msg,
            "sent" : None,
            "received": None,
            "sender" : self.server.sender,
        }
        self.to_send.put(msg)

    def flush_send(self):
        while not self.to_send.empty():
            try:
                msg = self.to_send.get()
                msg["sent"] = utils.get_time()
                msg = json.dumps(msg)
                utils.send_msg(self.c, msg)
            except:
                print("Could not deliver message to", self.server.addr)


    def shutdown(self):
        self.closed = True