'''
---------------------------------
Authors: 	    Ryan Karumanchery & Ramandeep Saini
Student IDs:    160349950 & 170627510
Date: 		    02/02/2020
Title: 		    CP372 Assignment One
Desc:		    Server for Note Application
---------------------------------
'''

# Import socket module
from socket import * 
# In order to terminate the program
import sys 

serverName = 'localhost'
# Assign a port number
serverPort = 6550

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
server_response = clientSocket.recv(1024)
print('From server: ', server_response.decode())

connected = True
while(connected):
    # POST 2 3 10 20 white new message here
    # Prompt for input
    command = input('Please enter a command <DISCONNECT, POST, GET, PIN, UNPIN, CLEAR>:')

    if (command == ""):
        print("Not enough arguments, please retry\n")
        continue

    # Encode and send command to server
    clientSocket.send(command.strip().encode())

    # Recieve response from server
    server_response = clientSocket.recv(1024)

    # Print server's response
    print('From server: ', server_response.decode())
    
    if (server_response.decode() == "DISCONNECTED"):
        connected = False
        # clientSocket.close()

clientSocket.close()