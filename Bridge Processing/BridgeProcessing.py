#!/usr/bin/env python
# coding: utf-8


#FDB
count = 0
fdb = {}
key = ""
with open("BridgeFDB.txt","r") as fh:
    lines = [line.rstrip('\n') for line in fh.readlines()]
    for line in lines:
        if count%2==0:
            key = line
        else:
            fdb[key] = line
        count = count + 1
print(fdb)



#Frames 
count = 1
frames = []
tempTup = []
with open("RandomFrames.txt","r") as fh:
    lines = [line.rstrip('\n') for line in fh.readlines()]
    for line in lines:
        if count%3==0:
            count=1
            #add three var tuple to frame
            tempTup.append(line)
            tempTup_ = tuple(tempTup)
            frames.append(tempTup_)
            tempTup = []
        else:
            #add into tuple
            tempTup.append(line)
            count = count + 1
print(frames)

        

#implementation
output = []
f= open("BridgeOutput.txt","w+")
for frame in frames:
    if frame[0] in fdb.keys():
        if frame[2] != fdb[frame[0]]:
            fdb[frame[0]] = frame[2]
    else:
        fdb[frame[0]] = frame[2]
    
    if frame[1] in fdb.keys():
        if frame[2] == fdb[frame[1]]:
            f.write(frame[0]+" "+frame[1]+" "+frame[2]+" "+"Discarded\n")
        else:
            f.write(frame[0]+" "+frame[1]+" "+frame[2]+" "+"Forwarded on port "+fdb[frame[1]]+"\n")
    else:
         f.write(frame[0]+" "+frame[1]+" "+frame[2]+" "+"Broadcast\n")

f.write("\n\nUpdated FDB:\n")
for key, value in fdb.items():
    f.write(key+" "+value+"\n")
f.close()




