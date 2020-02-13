import sys
from socket import *
import select

BUFF_SIZE = 1024                                                                                                                                                                                                #Create server socket

serverPort = int(sys.argv[1]) # getting the port number

#Making connection to the back-end server
serverAddr = ''  # localhost
clientToMainSocket = socket(AF_INET, SOCK_STREAM)
clientToMainSocket.connect((serverAddr,8888))
HTTPOK = "HTTP 1.0 200 OK \r\n\r\n"


#Make proxy server
proxyServer = socket(AF_INET,SOCK_STREAM)
proxyServer.bind((serverAddr,serverPort))
proxyServer.listen(5)
print("Lisetning on the local host, port :",serverPort)

def getMessage(msg):

	msgStart = msg.find("/")
	msgEnd = msg.find("HTTP")

	return msg[msgStart+1:msgEnd-1] + "\r\n\r\n"


while True:

	# Accept incoming connection
    clientSocket, clientAddr = proxyServer.accept()  # returns tuple

    print("Connected to client on ", clientAddr)

    while True:
        try:
            message = clientSocket.recv(BUFF_SIZE).decode()
            if message:

            	message = getMessage(message)  
                clientToMainSocket.send(message.encode())
                message = clientToMainSocket.recv(BUFF_SIZE).decode()
                clientSocket.send(HTTPOK)
                clientSocket.send(message.encode())
                clientSocket.close()

            else:
                readable, writable, errorable = select([],[], [clientSocket])
                for s in errorable:
                    s.close()
                break
        except:
            clientSocket.close()
            print("Connection closed")
            break

proxyServer.close()
clientToMainSocket.close()

#Testing sending and reciving one message Seemd to work.

'''testSentence = "test"
clientToMainSocket.send(testSentence.encode())
print(clientToMainSocket.recv(BUFF_SIZE).decode())
clientToMainSocket.close()
#test pushing ''' 

