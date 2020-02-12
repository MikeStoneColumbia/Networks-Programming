import sys
from socket import *
import select

BUFF_SIZE = 1024                                                                                                                                                                                                #Create server socket

serverPort = int(sys.argv[1]) # getting the port number

#Making connection to the back-end server
serverAddr = ''  # localhost
clientToMainSocket = socket(AF_INET, SOCK_STREAM)
clientToMainSocket.connect((serverAddr,8888))

#Make proxy server

proxyServer = socket(AF_INET,SOCK_STREAM)
proxyServer.bind((serverAddr,serverPort))
proxyServer.listen(5)
print("Lisetning on the local host, port :",serverPort)

while True:

	# Accept incoming connection
    clientSocket, clientAddr = proxyServer.accept()  # returns tuple

    print("Connected to client on ", clientAddr)

    while True:
        try:
            message = clientSocket.recv(BUFF_SIZE).decode()
            if message:
                print("Message from client: ", message)
                clientToMainSocket.send(message.encode())
                message = clientToMainSocket.recv(BUFF_SIZE).decode()
                print("Message to client: ", message)
            else:
                readable, writable, errorable = select([],[], [clientSocket])
                for s in errorable:
                    s.close()
                break
        except:
            clientSocket.close()
            print("Connection closed")
            break

#Testing sending and reciving one message Seemd to work.

'''testSentence = "test"
clientToMainSocket.send(testSentence.encode())
print(clientToMainSocket.recv(BUFF_SIZE).decode())
clientToMainSocket.close()
#test pushing ''' 

