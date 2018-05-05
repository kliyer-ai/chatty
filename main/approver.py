from threading import Thread, Event
import struct
import queue
import select
import json
from time import gmtime, strftime
import utils
from simpleHandler import SimpleHandler

class Approver(Thread):

    def __init__(self, server, c):
        Thread.__init__(self)
        Thread.daemon = True
        self.server = server
        self.c = c
        self.approved = Event()

    def run(self):
        msg = utils.recv_msg(self.c)
        msg = json.loads(msg)

        if "status" in msg and msg["status"] == "OK":
            user = msg["user"]
            self.server.pending[user] = self
            self.approved.wait()

            msg = {
            "status" : "OK",
            "user" : self.server.sender,
            "sent" : utils.get_time(),
            "received" : None
            }
            msg = json.dumps(msg)
            utils.send_msg(self.c, msg)

            handler = SimpleHandler(self.server, self.c)
            handler.start()

            self.server.users[user] = handler

        else:
            self.c.close()

