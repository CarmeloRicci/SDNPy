from socket import *

serverPort=4100


s = socket(AF_INET,SOCK_DGRAM)
# Bind the socket to the port
s.bind(('',serverPort))


while True:
    print("####### Server is listening #######")
    data, address = s.recvfrom(4096)
    print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")
