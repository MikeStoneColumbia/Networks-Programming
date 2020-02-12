import sys
from socket import *
import select

BUFF_SIZE = 1024                                                                                                                                                                                                #Create server socket

serverPort = str(sys.argv[1]) # getting the port number

#Making connection to the back-end server
serverAddr = ''  # localhost
clientToMainSocket = socket(AF_INET, SOCK_STREAM)
clientToMainSocket.connect((serverAddr,8888))

#Make proxy server

proxyServer = socke((AF_INET,SOCK_STREAM))
proxyServer.bind((serverAddr,serverPort))
proxyServer.listen(5)
print("Lisetning on the local host, port :",serverPort)

#Testing sending and reciving one message Seemd to work.

'''testSentence = "test"
clientToMainSocket.send(testSentence.encode())
print(clientToMainSocket.recv(BUFF_SIZE).decode())
clientToMainSocket.close()
#test pushing ''' 

