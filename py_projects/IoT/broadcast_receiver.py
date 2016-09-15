#!usr/bin/env python
import socket,sys
addr=('<broadcast>',10000)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.sendto('hello from client'.encode('utf-8'),addr)

def main():
    while True:
        data = s.recvfrom(1024)
        if not data:
            break
        pri10.tnt(data)

if __name__ == '__main__':
    main()
