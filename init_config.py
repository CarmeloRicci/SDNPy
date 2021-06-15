import subprocess
import socket
import sys
import ifaddr
import os
import time
import init_config

from configparser import ConfigParser
config = ConfigParser()
config.read('/etc/SDNPy-SDNWiMesh/config.ini')


def SetDeviceOnStart():
    temp = config.get(socket.gethostname(),'IpStation')
    os.system(f'uci set network.wlan.ipaddr={temp}')
    os.system('uci commit network')
    os.system('/etc/init.d/network restart')
    sys.stdout.flush()
    time.sleep(50)
    print("Tutto ok")

def GetIp(interface):
    adapters = ifaddr.get_adapters()

    temp = ""
    for adapter in adapters:
        if (adapter.nice_name == interface):
            temp = adapter.ips[0].ip
            print(interface + "--------------------------->", temp)
    
    return temp

    # addrs = netifaces.ifaddresses('br-wlan')
    # #print ( ((addrs[2])[0])['addr'] )
    # return ((addrs[2])[0])['addr']

def GetDefaultGateway(interface):
    temp = GetIp(interface)
    temp1 = temp.split(".")
    temp2 = "" + temp1[0] + "." + temp1[1] + "." + temp1[2] + "." + "1"
    #print ( temp1 , type(temp1) )
    return temp2

    # gateway = ''
    # addrs = netifaces.ifaddresses(interface)
    # print ( addrs )

    # for obj in netifaces.gateways()[2]:
    #     if ( ((obj)[0])[1] == interface ):
    #         gateway = ((obj)[0])[0]
    # return gateway


def GetNeighboors():
    neigh=[]
    #flag=True
    #while flag:
    result = subprocess.Popen("fping -A -D -a -q -g -a -i 1 "+str(config['GENERAL']['IpSink'])[:-1]+"0/24", shell=True, stdout=subprocess.PIPE)
    s = result.stdout.read()
    s1 = s.decode('utf-8', 'ignore')
    neigh = s1.splitlines()
    neigh.remove(init_config.GetIp(config['GENERAL']['StationInterface']))        
        #size = len(list)
    print("Network Scanning..arp stabilizing")
        #if size < int(config['GENERAL']['NumberOfNodes']):
            #print("Arp table size:", len(list))
            #flag = False
        #for h in list:
            #neigh.append(h)
                #field = h.split(" ")
                #if str(config['GENERAL']['IpSink'])[:-2] in str(field[0]) and str(field[2]) == "br-lan" and str(field[5]) != "router" and str(field[8]) != "FAILED":
        

    return neigh




def FlusSystem():    
    os.system("ip neigh flush ./")
    subprocess.Popen("fping -A -D -a -q -g -a -i 1 "+str(config['GENERAL']['IpSink'])[:-1]+"0/24", shell=True, stdout=subprocess.PIPE)    
    sys.stdout.flush()
    #os.system("ping -c 1 192.168.3."+str(i+1))
    sys.stdout.flush()
    os.system("rm -rf /tmp/luci*")
    sys.stdout.flush()
    os.system("sync | echo 3 > /proc/sys/vm/drop_caches")
    sys.stdout.flush()

    
    return
