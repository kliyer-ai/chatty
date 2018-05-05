from threading import Thread
import struct
import queue
import select
import json
from time import gmtime, strftime
import utils
from simpleHandler import SimpleHandler

class Connector(Thread):

    def __init__(self, server ,c, msg):
        Thread.__init__(self)
        Thread.daemon = True
        self.server = server
        self.c = c
        self.msg = msg

    def run(self):
        msg = {
            "status" : "OK",
            "user" : self.server.sender,
            "sent" : utils.get_time(),
            "received" : None
        }
        msg = json.dumps(msg)
        utils.send_msg(self.c, msg)

        answer = utils.recv_msg(self.c)
        answer = json.loads(answer)

        if "status" in answer and answer["status"] == "OK":
            recipient = answer["user"]
            handler = SimpleHandler(self.server, self.c)
            handler.start()
            handler.send(self.msg)

            self.server.users[recipient] = handler
        else:
            self.c.close()