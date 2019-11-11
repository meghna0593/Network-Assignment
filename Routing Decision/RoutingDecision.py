#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import socket
import struct

#Packets
with open("RandomPackets.txt",'r') as fp:
    packets = [line.rstrip('\n') for line in fp.readlines()]

#Routing Table
#assuming that set of 8 bits can have continuous 1s on subnet mask 
with open("RoutingTable.txt",'r') as fp:
    lines = [line.rstrip('\n') for line in fp.readlines()]
    mask = []
    destn = []
    nxtHop = []
    intfc = []
    for i in range(0,len(lines)):
        if i%3 == 0: 
            destn.append(lines[i].split("/")[0])
            mask.append(socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - int(lines[i].split("/")[1]))) & 0xffffffff)))
        elif i%3 == 1:
            nxtHop.append(lines[i])
        else:
            intfc.append(lines[i])
    mask = set(mask)
    mask = sorted(mask,reverse=True)

#Dataframe of routing table
df = pd.DataFrame({ "destn":destn, 
                    "next_hop":nxtHop,
                    "interface":intfc
                  }) 

#Main operation after arraging data
output = []
f= open("RoutingOutput.txt","w+")
for i in packets:
    firstQuad = int(i.split(".")[0])
    if (firstQuad < 223):
        if(firstQuad == 127):
            f.write(i+" is loopback; discarded\n")
        else:
            #forward packets based on masks
            for j in mask:
                #AND operation
                trailzero = len(''.join(j.split("."))) - len(''.join(j.split(".")).rstrip('0'))
                updatIp = i.split(".")
                for k in range(0,trailzero):
                    updatIp[len(updatIp)-1-k]='0'
                updatIp = '.'.join(updatIp)
                
                #retrieving packets and forwarding them
                if(df['destn'].str.contains(updatIp).any()):
                    temp = df[df.destn == updatIp]
                    f.write(i+' will be forwarded'+(' on the directly connected network on interface ' if temp['next_hop'].values[0]=='-' else ' to '+temp['next_hop'].values[0]+' out on interface ')+temp['interface'].values[0]+'\n')
                    break
                
    else:
        f.write(i+" is malformed; discarded\n")
f.close()


#References
#1. How to convert a CIDR prefix to a dotted-quad netmask in Python? (n.d.). Retrieved November 8, 2019, from https://stackoverflow.com/questions/23352028/how-to-convert-a-cidr-prefix-to-a-dotted-quad-netmask-in-python.

