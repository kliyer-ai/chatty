import argparse
from server import Server
from client import Client

def main(addr, mode):

    if mode == "s":
        s = Server(addr)
        s.start()
    elif mode == "c":
        c = Client(addr)
        c.send()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest = "port", default = "4444", help="port")
    parser.add_argument("-ip", "--ipaddress", dest = "ip", default = "127.0.0.1", help="ip address to connect to")
    parser.add_argument("-m", "--mode", dest="mode", default="c")

    args = parser.parse_args()
    
    main((args.ip, int(args.port)), args.mode)