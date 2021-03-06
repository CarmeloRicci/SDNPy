from Packets import BeaconPacket
from Packets import ReportPacket
from Packets import Packets
import init_config
import socket
import ifaddr
import subprocess
import os
import time
import UDP_Socket
import AudioFile
import threading
import node_variables
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


############ 0. Asseganre gli Indirizzi Ip Nuovi ############

print("\n\n\t\tSTART SDNWISE\n\n")

init_config.SetDeviceOnStart()

print("\n\tIndirizzi Ip Asseganti\n")


############ 1. Calcolo Indirizzi Ip Nuovi ############
node_variables.IpStation = init_config.GetIp( config['GENERAL-OMEGA']['StationInterface'] )
node_variables.IpClient = init_config.GetIp( config['GENERAL-OMEGA']['ClientInterface'] )

print(f'Client: {node_variables.IpClient} \t Station: {node_variables.IpStation}')

node_variables.IpDefaultGateway = init_config.GetDefaultGateway( config['GENERAL-OMEGA']['ClientInterface'] )

print(f"Default Gateway: {node_variables.IpDefaultGateway}")

############ 2. Run Threads ############
if (config.get(socket.gethostname(),'Sink') == "SI"):
    node_variables.IpClient = node_variables.IpStation

ThreadUdpReceiver = UDP_Socket.ThreadReceiverUdpPackets(1, "Thread-UdpReceiver", int(config['GENERAL']['Port']) )

pckBeacon = BeaconPacket ( config.get(socket.gethostname(),'NetId'), node_variables.IpDefaultGateway , node_variables.IpStation, "100", node_variables.IpDefaultGateway, config.get(socket.gethostname(),'Id') + " " + node_variables.IpClient )
ThreadUdpBeacon = UDP_Socket.ThreadBeacon( 2, "Thread-Beacon", pckBeacon.getBytesFromPackets() , int(config['GENERAL']['Port']) )

if (config.get(socket.gethostname(),'Sink') == "NO"):
    ThreadUdpReport = UDP_Socket.ThreadReport(3, "Thread-Report", int(config['GENERAL']['Port']), node_variables.IpClient, node_variables.IpDefaultGateway ) 
else:
    ThreadUdpReport = UDP_Socket.ThreadReport(3, "Thread-Report", int(config['GENERAL']['Port']), node_variables.IpStation, node_variables.IpDefaultGateway ) 

ThreadPrintInfo = UDP_Socket.ThreadPrintInfoNode(4,"Thread-Info")

if (config.get(socket.gethostname(),'Sink') == "NO"):
    ThreadUdpBeacon.start()

ThreadAudioFile = AudioFile.ThreadSendDataAudio(4,"Tread-Audio")

ThreadUdpReceiver.start()
ThreadUdpReport.start()
ThreadPrintInfo.start()
ThreadAudioFile.start()


############ 2. Avvio Server UDP ############


# UDP_Socket.RunReceiverProcess(IpStation,4000)
# UDP_Socket.ReceiverPacket(IpStation)

# while True:
#     UDP_Socket.SendPacket("Ciao","192.168.0.130")



# MULTICAST


# if ( socket.gethostname() == "Omega-1D63"):
#     server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#     server.settimeout(0.2)
#     message = b"your very important message"
#     while True:
#         server.sendto(message, ('<broadcast>', 37020))
#         print("message sent!")
#         time.sleep(1)

# if ( socket.gethostname() == "Omega-1D06"):
#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
#     client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#     client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#     client.bind(("", 37020))
#     while True:
#         data, addr = client.recvfrom(1024)
#         print("received message: %s"%data)



# PACKETS


# p1 = BeaconPacket("1","10.10.0.1","10.10.0.0","100","10.10.0.1")
# print(p1.printFullPacket())
# print(p1.printLitePacket())

# p1.getBytesFromPackets() 

# test = bytearray(b'-1--46------10.10.0.1------10.10.0.0-0100------10.10.0.1Payload BEACON')
# p2 = Packets.getPacketFromBytes(test)

# print(p2.printFullPacket())
# print(p2.printLitePacket())

