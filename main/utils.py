import struct
import time

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = bytes(msg, 'utf-8')
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    raw_msg = recvall(sock, msglen)
    return str(raw_msg, 'utf-8')

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
    
def get_time():
    return time.strftime("%d, %m, %Y %H:%M:%S", time.gmtime())