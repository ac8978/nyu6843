from socket import *
import statistics
import os
import sys
import struct
import time
import select
import binascii
# Should use stdev

ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        icmp_header = recPacket[20:28]
        type, code, check_sum, packetid, seq = struct.unpack("bbHHh", icmp_header)
        bytes = struct.calcsize("d")
        timeSent = struct.unpack("d", recPacket[28: 28 + bytes])[0]
        timeDiff = (timeReceived - timeSent) * 1000
        ip_header = recPacket[:20]
        version, type, length, id, flags, ttl, protocol, checksum, src_ip, dest_ip = struct.unpack("BBHHHBBH4s4s", ip_header)
        #unpacked_data = struct.unpack(struct_format , ip_header)
        ttl = ip_header[5]
        return(bytes, timeDiff,ttl)
    
    
        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)


    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")


    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,  	# the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Calculate vars values and return them
    #  vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]

    #reguarl code
    packet_list = []
    packet_min = 9999999999999999999999.00
    packet_max = 0.00
    packet_avg = 0.00
    stdev_var = 0.00
    
    
    
    
    # Send ping requests to a server separated by approximately one second
    for i in range(0,4):
        #reguarl code
        delay = doOnePing(dest, timeout)
        if float(delay[1]) < float(packet_min):
            packet_min = delay[1]
        if float(delay[1]) > float(packet_max):
            packet_max = delay[1]
        packet_list.append(float(delay[1]))
        print("Reply from " + dest + ": bytes=" + str(delay[0]) + " time=" + str(delay[1]) + "ms TTL=" + str(delay[2]))
        #reguarl code
        time.sleep(1)  # one second

    packet_avg = statistics.mean(packet_list)
    stdev_var = statistics.pstdev(packet_list)
    vars = [float(round(packet_min, 2)), float(round(packet_avg, 2)), float(round(packet_max, 2)),float(round(stdev_var, 2))]
            
    return vars

if __name__ == '__main__':
    #ping("google.com")
    #ping("google.ru")
    #ping("google.mx")
    ping("127.0.0.1")
    
