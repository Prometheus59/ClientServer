# Import socket module
from socket import * 
import sys # In order to terminate the program


colors = []

port_number = sys.argv[1]
board_width  = sys.argv[2]
board_height = sys.argv[3]

for x in sys.argv[4:]:
	colors.append(x)

for x in colors:
	print("Color added: " + str(x))


def __init__(self, port_number, board_width, board_height, colors):
	self.port_number = port_number
	self.board_width = board_width
	self.board_height = board_height
	self.colors = colors

notes = []
pins = []

def main(string):
	arr = string.split(" ",6)

	if arr[0].upper() == 'POST':
		new_note = note(arr[1], arr[2], arr[3], arr[4], arr[5], arr[6])
		post(new_note)
	elif arr[0].upper() == 'GET':
		get()
	elif arr[0].upper() == 'CLEAR':
		clear()
	elif arr[0].upper() == 'PIN':
		pin(arr[1])
	elif arr[0].upper() == 'DISCONNECT':
		disconnect()

class note:
	def __init__(self, coord_x, coord_y, width, height, color, message):
		self.coord_x = coord_x
		self.coord_y = coord_y
		self.width = width
		self.height = height
		self.color = color
		self.message = message
		self.status = 0

def post(note_obj):
	notes.append(note_obj)
	print(note_obj)

def get():
	return 1

def clear():
	return 1

def pin():
	return 1

def disconnect():
	serverSocket.close()
	sys.exit()



# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 1 connection at a time TODO: Allow for multiple connections?
serverSocket.listen(1)

print ('Server setup complete')

# Server should be up and running and listening to the incoming connections

while True:
	print('The server is ready to receive')

	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()

	# Get client's command
	#1024 is maximum amount of data to be recieved
	string = connectionSocket.recv(1024).decode()
	main(string)
	
	# Perform function/command (POST/GET/PIN/UNDERPIN/CLEAR/DISCONNECT)
	# capitalizedSentence = sentence.upper()

	# Send results back to client
	# connectionSocket.send(capitalizedSentence.encode())
	connectionSocket.send(string.encode())

	# End connection with client
	connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
