import sys
from socket import *
import select

BUFF_SIZE = 1024                                                                                                                                                                                                #Create server socket

serverPort = str(sys.argv[1]) # getting the port number
serverAddr = ''  # localhost
clientToMainSocket = socket(AF_INET, SOCK_STREAM)
clientToMainSocket.connect(('',8888))
testSentence = "test"
clientToMainSocket.send(testSentence.encode())
print(clientToMainSocket.recv(BUFF_SIZE).decode())
clientToMainSocket.close()