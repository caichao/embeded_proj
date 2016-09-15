#!usr/bin/env python
import socket

host=''
port = 10000
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.bind((host,port))

def main():
    while True:
        try:
            data,addrs = s.recvfrom(1024)
            print("got data from",addrs)
            s.sendto('broadcasting'.encode('utf-8'),addrs)
            print(data)
        except KeyboardInterrupt:
            raise
        
if __name__ =='__main__':
    main()
