"""
sample proxy program for Part 2
Computer Networks Spring 2020

"""

from socket import *
from re import *
import select
import sys
import os

BUFF_SIZE = 1024

def sendToServer(serverSocket, request, domain):
    # Send GET request to server socket
    # Does not return anything

    ## Your code here ##
    pass 

def receiveFromServer(serverSocket):
    # Receive message from socket
    # Returns a tuple (body, response header)
    # Uses nonblocking select call (timeout=0)

    ## Your code here ##

    return body, responseLine

​
def createProxySocket():
    # Create socket to listen on
    # return socket

    ## Your code here ##
    
    return proxySocket

def connectSocket(domain, serverPort):
    # Connect to server
    # Return serverSocket

    ## Your code here ##
​
    return serverSocket

def checkCache(fileName, path, domain, serverPort):
    # Checks cache for file
    # appends index.html to a request for a directory
    # returns the body and response code from the server
​
    ## Your code here ##

    # Check if the request exists in cache
    if os.path.exists(fileName):
       ## Your code here ## 
​
        with open(fileName, "rb") as f:
            ## Your code here ##
            f.read('''Your code here''')
​
    else:
        ## Your code here ##
        with open(fileName, "wb") as f:
            f.write('''Your code here''')
​
​
    return body, responseLine

def main():
    # Define server socket address
    serverPort = 80
​
    # Create proxy socket
    proxySocket = createProxySocket()
​
​
    while True:
        clientSocket, clientAddr = proxySocket.accept()  # Accept a connection
​
        readable, _, _ = select.select([clientSocket], [], [], 0)
        if readable:
            # Receive 1024 bytes from client
            clientMessage = clientSocket.recv(BUFF_SIZE).decode(errors='ignore')
            print("\nClient message : \n****\n" + clientMessage + "\n****\n" )
​
            # Parse requests
            request = clientMessage.split(" ")[1]  # first line is "GET /path HTTP/1.0\r\n" so we want /path/
            
            ## Your code here ##
​
            body, responseLine = checkCache(sysPath, path, domain, serverPort)
​
            # Send data back to client
            
​            ## Your code here ##

            clientSocket.close()  # close socket to wait for new request
        else:
            # Or other error handling 
            clientSocket.close()
​
    proxySocket.close()
​
if __name__ == "__main__":
    main()