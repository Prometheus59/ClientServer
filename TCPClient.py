# Import socket module
from socket import * 
import sys # In order to terminate the program

serverName = 'localhost'
# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

#a = "POST 2 3 10 20 white"
# Prompt for input
command = input('Enter Command (POST, GET, PIN/UNPIN, CLEAR, DISCONNECT):')

# Encode and send command to client
clientSocket.send(command.encode())

# Recieve response from server
user_input = clientSocket.recv(1024)

# Print server's response
print('From server: ', user_input.decode())
clientSocket.close()