from socket import *
import os
import sys
import struct
import time
import select
import binascii 

ICMP_ECHO_REQUEST = 8
TIMELIMIT = 3.0
ATTEMPTS = 3 
HOPS = 64
results = {}
flag = 0


def checksum(string): # this was retrieved from the IcmpPing.py
    csum = 0
    countTo = (len(string) // 2) * 2  
    count = 0

    while count < countTo:
        thisVal = string[count+1] * 256 + string[count] 
        csum = csum + thisVal 
        csum = csum & 0xffffffff  
        count = count + 2
    
    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff 
    
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum 
    answer = answer & 0xffff 
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer 

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the #dummy header.

    myChecksum = checksum(header + data) 
    
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff     
    else:
        myChecksum = htons(myChecksum)
        
    header = struct.pack("BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not string
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    global flag
    while True: 
        t = time.time()
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            results[timeout] = "Packet Times out "
            return -1
    
        timeReceived = time.time() 
        recPacket, addr = mySocket.recvfrom(1024)
        
        timeRemaining = timeLeft - howLongInSelect 

        if timeLeft <= 0:
            results[timeout] = "Packet Times out"
            return -1
        
        # Fetch the ICMPHeader from the received IP
        #Fill in start

        icmp = recPacket[20:28]

        icmpType, code, checksum, packetID, sequence = struct.unpack('bbHHh',icmp)

        ttl = "%.0f" % ((timeReceived - t)*1000)

        if icmpType == 0:
            bytes = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytes])[0]

            if timeout not in results:

                results[timeout] = str(addr[0]) + ": " + ttl + "ms "
            else:    
                results[timeout] = results[timeout] + ttl + "ms "

            flag += 1
            return icmpType

        elif icmpType == 11:
            bytes = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytes])[0]

            if timeout not in results:

                results[timeout] = str(addr[0]) + ": " + ttl+ "ms " 
            else:    
                results[timeout] = results[timeout] + ttl + "ms "

            return icmpType

        elif icmpType == 3:
            bytes = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytes])[0]

            if timeout not in results:

                results[timeout] = str(addr[0]) + ": " + ttl + "ms "
            else:    
                results[timeout] = results[timeout] + ttl + "ms "

            return icmpType

        
            
        return 0
    
def doOnePing(destAddr, timeout): 
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', timeout))
    mySocket.settimeout(TIMELIMIT)
    
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    icmpType = receiveOnePing(mySocket, myID, timeout, destAddr)
    
    mySocket.close()
    return icmpType


def findRoute(hostname):
    dest = gethostbyname(hostname)
    print("Find the route to " + hostname + " using Python3")
    print("TIMELIMIT set to 3.0 seconds")
    print("")
    timelimit = TIMELIMIT
    reset()
    global flag

    for hop in range(1,HOPS+1):
        for attempt in range(ATTEMPTS):
            icmpType = doOnePing(dest,hop)
            if(flag == ATTEMPTS):
                print(str(hop) + "\t" + results[hop] + "\n")
                flag = 0
                return;
            if icmpType == -1 :
                break;
        print(str(hop) + "\t" + results[hop] + "\n")


def reset():
    results.clear()
    

if __name__ == '__main__':  
    '''findRoute("www.google.com")
    findRoute("Ozbargain.com.au") # some australian website
    findRoute("ww.facebook.com")
    findRoute("Vklass.se") # some swedish site
    findRoute("127.0.0.1") #localhost'''

    while True:

        link = str(input("please enter the host name you want to traceroute: "))
        findRoute(link)

    












