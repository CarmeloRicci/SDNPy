import threading
import socket
import sys
import time
import PacketsHandler
from Packets import ReportPacket
from Packets import BeaconPacket
from Packets import Packets
import node_variables
from configparser import ConfigParser
import init_config
config = ConfigParser()
config.read('/etc/SDNPy-SDNWiMesh/config.ini')
ttl=1
# --- Thread Receiver Udp Packets --- #
class ThreadReceiverUdpPackets (threading.Thread):
   def __init__(self, threadID, name, port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.port = port

   def run(self):
       print("Starting " + self.name)
       #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
       UdpSocketReceiverFromNode( self.port )
       

def UdpSocketReceiverFromNode(port):
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (init_config.GetIp(config['GENERAL']['StationInterface']), port)
    s.bind(server_address)
   
    while True:
       print("####### Node is listening #######")
       data, address = s.recvfrom(8192)
       #s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
       #print("\n\n 2. Node received: ", data.decode('utf-8'), "\n\n")
       PacketsHandler.PacketHandler(data,address)


class ThreadReceiverUdpPacketsFromController (threading.Thread):
   def __init__(self, threadID, name,ip,port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.port = port
      self.ip= ip

   def run(self):
       print("Starting " + self.name)
       #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
       UdpSocketReceiverFromController(self.ip, self.port )


def UdpSocketReceiverFromController(ip,port):
    # Create a UDP socket
    #sC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sC = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # Bind the socket to the port
    #server_address = (ip, port)
    sC.bind(('',port))



    while True:
       print("####### Node is listening #######")
       data, address = sC.recvfrom(4096)
       #s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
       #print("\n\n 2. Node received: ", data.decode('utf-8'), "\n\n")
       PacketsHandler.PacketHandler(data,address)


# --- Thread Beacon Udp Packets --- #
class ThreadBeacon (threading.Thread):
   def __init__(self, threadID, name, beacon, ip, port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.beacon = beacon
      self.port = port
      self.ip = ip

   def run(self):
      print ("Starting " + self.name)
      SendUdpPacketBroadcastLoop(self.beacon, self.ip,self.port)

def SendUdpPacketBroadcastLoop(beacon,ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
   print("Do Ctrl+c to exit the program !!")
   # Let's send data through UDP protocol
   while True:     
      s.sendto(beacon, (ip, port))
      print("\n\n 1. Node Send Beacon: ", beacon, "\n\n")
      # close the socket
      print("Beacon Send!")
      time.sleep(int(config['GENERAL']['BeaconSleep']))


# --- Thread Report Udp Packets --- #
class ThreadReport (threading.Thread):
   def __init__(self, threadID, name, port, s_address, d_address):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.port = port
      self.s_address = s_address
      self.d_address = d_address

   def run(self):
      print ("Starting " + self.name)
      SendUdpPacketUnicastLoop(self.port, self.s_address, self.d_address)






def SendUdpPacketUnicastLoop(port,src,dst):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
   print("Do Ctrl+c to exit the program !!")
   # Let's send data through UDP protocol
   while True:
      neigh=init_config.GetNeighboors()
      pckReort = ReportPacket ( config['GENERAL']['NetId'], dst, src, config['GENERAL']['TTL'], dst, ", ".join(neigh))
      bytesToSend = pckReort.getBytesFromPackets() 
      s.sendto(bytesToSend, (dst, port))
      print("\n\n 1. Node Send Report : ", bytesToSend, "\n\n")
      # close the socket
      print("Unicast Report Send!")
      time.sleep(int(config['GENERAL']['BeaconSleep']))


     

  


# --- Generic Function For Send Udp Packets --- #

def SendUdpPacketUnicast(data,address,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
   s.sendto(data, (address, port))
   print("\n\n 1. Packet sent: ", data, "\n\n")




class ThreadPrintInfoNode (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
       print("Starting " + self.name)
       #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
       PrintBasicInfo(1,0)

def PrintBasicInfo(NeighborInfo,OtherInfo):
    while True:
      print("\n[B-INFO] Network ID: ", config.get(socket.gethostname(),'NetId') )
      print("[B-INFO] Node ID: ", config.get(socket.gethostname(),'Id') )
      print("[B-INFO] SINK: ", config.get(socket.gethostname(),'Sink') )
      print("[B-INFO] Ip Station: ", node_variables.IpStation )
      print("[B-INFO] Ip Client: ", node_variables.IpClient )
      print("[B-INFO] Default Gateway: ", node_variables.IpDefaultGateway )
      if (NeighborInfo == 1):
         print("[Nei-INFO] Network ID: ", node_variables.list_neighbor )
      if (OtherInfo == 1):
         print(" --- ")
      print("\n")
      time.sleep(int(config['GENERAL']['InfoSleep']))




class ThreadFlusSystem(threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      while True:
         print("Starting " + self.name)
         init_config.FlusSystem()
         time.sleep(int(config['GENERAL']['ScanNetSleep']))
         