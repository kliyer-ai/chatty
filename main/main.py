import argparse
from client import Client

def main(addr, user):
    client = Client(addr, user)

    done = False
    while not done:
        inp = input("Choose option:").split(" ")
        command = inp[0]
        if command == "send":
            client.send()
        elif command == "receive":
            client.get_msgs()
        elif command == "pending":
            client.pending()
        elif command == "approve":
            client.approve(inp[1])
        elif command == "done":
            done = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest = "port", default = "4444", help="port")
    parser.add_argument("-ip", "--ipaddress", dest = "ip", default = "", help="ip address to connect to")
    parser.add_argument("-u", "--user", dest = "user", default = "anonymous", help="Your user name")

    args = parser.parse_args()
    
    main((args.ip, int(args.port)), args.user)