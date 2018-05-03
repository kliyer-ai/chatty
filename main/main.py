import argparse
from client import Client

def main(addr, user):
    client = Client(addr, user)

    done = False
    while not done:
        command = input("Choose option")
        if command == "send":
            client.send()
        elif command == "receive":
            client.get_msgs()
        elif command == "done":
            done = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest = "port", default = "4444", help="port")
    parser.add_argument("-ip", "--ipaddress", dest = "ip", default = "127.0.0.1", help="ip address to connect to")
    parser.add_argument("-u", "--user", dest = "user", default = "anonymous")

    args = parser.parse_args()
    
    main((args.ip, int(args.port)), args.user)