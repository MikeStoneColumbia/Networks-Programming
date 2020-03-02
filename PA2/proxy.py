"""
sample proxy program for Part 2
Computer Networks Spring 2020

"""

from socket import *
from re import *
from datetime import datetime
import select
import sys
import os

BUFF_SIZE = 1024

userPort = int(sys.argv[1])
serverAddr = ''

print(datetime.now())

def sendToServer(serverSocket, request, domain):
    # Send GET request to server socket
    # Does not return anything

    ## Your code here ##
     path = request.split(" ")[1]
     newRequest = request.split("\r\n")[0] # This is the first line of the response
     offset = len(domain) + 5 #skips the domain
     httpOffset = newRequest.find("HTTP")

     if(path[-1] == "/"):
        newRequest = "GET " + newRequest[offset:httpOffset-1] + "index.html " + "HTTP/1.0" + "\r\n\r\n"
    
     else:
        newRequest = "GET " + newRequest[offset:httpOffset] + "HTTP/1.0" + "\r\n\r\n"

     '''print("The request being sent: ")
     print(newRequest)
     print("******")'''

     serverSocket.send(newRequest)



def receiveFromServer(serverSocket):
    # Receive message from socket
    # Returns a tuple (body, response header)
    # Uses nonblocking select call (timeout=0)

    ## Your code here ##
    dataLen = BUFF_SIZE
    test = ""

    while 1:
        temp = serverSocket.recv(BUFF_SIZE)
        if not temp:
            break
        test += temp

    body = test.split("\r\n\r\n")[1]
    responseLine = test.split("\r\n\r\n")[0]

    '''print("The responseLine: ")
    #print(test.split("\r\n")[0])
    print(responseLine)
    print("******")'''

    '''print("The body: ")
    print(body)
    print("******")'''

    return body, responseLine

def createProxySocket():
    # Create socket to listen on
    # return socket
    ## Your code here ##

    proxySocket = socket(AF_INET,SOCK_STREAM)
    proxySocket.bind((serverAddr,userPort))
    proxySocket.listen(5)
    print("Lisetning on the local host, port :",userPort)
    
    return proxySocket

def connectSocket(domain, serverPort):
    # Connect to server
    # Return serverSocket

    ## Your code here ##
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((domain,serverPort))
    return serverSocket

def checkCache(fileName, path, domain, serverPort):
    # Checks cache for file
    # appends index.html to a request for a directory
    # returns the body and response code from the server
    ## Your code here ##

    # Check if the request exists in cache
    if os.path.exists(fileName):
       ## Your code here ## 
        #print("path does exist")
        with open(fileName, "rb") as f:
            ## Your code here ##
            next(f)

            body = ""

            for line in f:
                body += line
            responseLine = "HTTP/1.1 200 OK"

    else:
        ## Your code here ##
        
        #print("does not exist")
        body,responseLine = path

        parts = fileName.split("/")
        directoryPath = ""

        for part in parts[:-1]:
            directoryPath += part;
            directoryPath += "/"

        if(os.path.exists(directoryPath)):
            with open(fileName, "wb") as f:
                f.write(str(datetime.now())+"\n")
                f.write(body)

        else:    
            os.makedirs(directoryPath)
            with open(fileName, "wb") as f:
                f.write(str(datetime.now())+"\n")
                f.write(body)

    serverPort.close()
    return body, responseLine

def handle301(responseLine, domain):

    location = responseLine.split("Location: ")[1]
    
    url = location.split("\r\n")[0]
    path = url.split("//")[1]
    #
    ("Here is the url: " + path)
    response = url.split(domain)[1]

    if(response[-1] == "/"):
        newRequest = "GET " + response + "index.html " + "HTTP/1.0" + "\r\n\r\n"
    
    else:
        newRequest = "GET " + response + "HTTP/1.0" + "\r\n\r\n"

    return newRequest, " "+ path + "index.html"

def getDomain(request):

    return request.split("/")[1]

def main():
    # Define server socket address
    serverPort = 80

    # Create proxy socket
    proxySocket = createProxySocket()


    while True:
        clientSocket, clientAddr = proxySocket.accept()  # Accept a connection
        
        readable, _, _ = select.select([clientSocket], [], [], 0.5)

        if readable:
            # Receive 1024 bytes from client

            clientMessage = clientSocket.recv(BUFF_SIZE).decode(errors='ignore')
            #print("\nClient message : \n****\n" + clientMessage + "\n****\n" )

            # Parse requests

            #print(len(clientMessage))

            path = ""

            if(len(clientMessage) > 0):
                request = clientMessage.split(" ")[1]  # first line is "GET /path HTTP/1.0\r\n" so we want /path/
                domain = getDomain(request) #gets us the domain we are trying to connect to.
                firstLine = clientMessage.split("\r\n")[0]
                path = firstLine.split(" ")[1]
                if(path[-1] == '/'):
                    path += "index.html"
                #print(path[1:])
                #print("The domain is this.",domain)

            else:
                domain = ""
                
            ## Your code here #

            if (".com" in domain) or (".edu" in domain) or (".org" in domain) :

                #print("made it in here")
                webSocket = connectSocket(domain,serverPort) # connected to the website
                
                sendToServer(webSocket,clientMessage,domain)
                body,responseLine = receiveFromServer(webSocket)
                if "301 Moved Permanently" in responseLine:
                    webSocket.close()
                    webSocket = connectSocket(domain,serverPort)
                    newRequest,path = handle301(responseLine,domain)
                    webSocket.send(newRequest)
                    body,responseLine = receiveFromServer(webSocket)

                body, responseLine = checkCache(path[1:], (body,responseLine), domain, webSocket)
                

                clientSocket.send(responseLine+"\r\n\r\n")
                clientSocket.send(body+"\r\n\r\n")
                


            else:
                clientSocket.send("HTTP/1.1 200 OK\r\n\r\n")

            

           

            # Send data back to client
            
           ## Your code here ##

            clientSocket.close()  # close socket to wait for new request
            #print("socket closed")
        else:
            # Or other error handling 
            clientSocket.close()

    proxySocket.close()

if __name__ == "__main__":
    main()