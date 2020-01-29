# Import socket module
from socket import * 
import sys # In order to terminate the program

# For testing: python TCPServer.py 6550 200 100 red white blue

colors = []

port_number = sys.argv[1]
board_width  = sys.argv[2]
board_height = sys.argv[3]

# Add colors
for x in sys.argv[4:]:
	colors.append(x)

for x in colors:
	print("Color added: " + str(x))

class board:
	def __init__(self, port_number, board_width, board_height, colors):
		self.port_number = port_number
		self.board_width = board_width
		self.board_height = board_height
		self.colors = colors

# This is shared between all clients (share object)
main_board = board(port_number, board_width, board_height, colors)

notes = []
pins = []

def main(string):
	arr = string.split(" ",1)

	if arr[0].upper() == 'POST':
		arr = string.split(" ", 6)
		new_note = note(arr[1], arr[2], arr[3], arr[4], arr[5], arr[6])
		return post(new_note)
	elif arr[0].upper() == 'GET':
		return get(string)
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
	
	# comparing
	def __eq__(self, other):
		if self.coord_x == other.coord_x and self.coord_y == self.coord_y \
		and self.width==other.width and self.height == other.height \
		and self.color == other.color and self.message == other.message:
			return True
		else:
			 return False
	
	def __str__(self):
		return f'{self.coord_x} {self.coord_y} {self.width} {self.height} {self.color} {self.message}'
	
	def check_dimensions(self):
		if (int(self.coord_x) + int(self.width)) > int(main_board.board_width) or \
			(int(self.coord_y) + int(self.height)) > int(main_board.board_height):
			return False
		else:
			return True

# Post incomplete - Must account for board information (height, color)
def post(note_obj):
	# if (note fits dimensions of board)
	"""
	if (int(note_obj.height) + int(note_obj.coord_y)) < int(main_board.board_height) and \
		(int(note_obj.width) + int(note_obj.coord_x))<main_board.board_width:
		
		return "Message Posted" + str(note_obj.message)
		"""
	if note_obj.check_dimensions():
		notes.append(note_obj)
		return "note posted"
	else:
		print("Note height is " + note_obj.height + note_obj.coord_y)
		print(main_board.board_height)
		return "Message not posted: Insufficient space on board"
	# print("note posted: " + note_obj.message)


def get(string):

	"""
	arg = string.split(" ", 1)
	if ("referes" in arg):
		text = arg.split("=",1)

	arg1 = note_search[1]
	arg1_command = arg1.split("=")
	if (arg1_command == "color"):
	"""
	command = string.replace("="," ").split()
	try:
		color_index = command.index("color")
	except ValueError:
		color_index = -1
	try:
		contain_index = command.index("contains")
	except ValueError:
		contain_index = -1
	try:
		refers_index = command.index("refersTo")
	except ValueError:
		refers_index = -1

	if color_index != -1:
		new_color = command[color_index+1]
	else:
		new_color = ""
	if  contain_index != -1:
		new_x_coord = command[contain_index+1]
		new_y_coord = command[contain_index+2]
	else:
		new_x_coord = new_y_coord = ""
	if refers_index != -1:
		new_reference = command[contain_index:]
		new_text = ' '.join(new_reference)
	else:
		new_text = ""

	notes_returned = notes.copy()
	
	for i in notes_returned:
		#if (color_index != -1 and i.color!=new_color):
			
		if ((color_index != -1 and str(i.color) != str(new_color)) or \
			(contain_index != -1 and (str(i.coord_x) != str(new_x_coord) or \
				str(i.coord_y) != str(new_y_coord))) or \
				(refers_index != -1 and str(new_text) not in str(i.message))):
			notes_returned.remove(i)
			print("Note: " + i.message + " :removed from temp list\n")

	# send to client
	obj_string = "\n"
	for x in notes_returned:
		obj_string += str(x) + "\n"

	return obj_string

"""
	for i in notes:
		if new_color == i.color:
			if i not in notes_returned:
				notes_returned.append(i)
		if new_x_coord == i.coord_x:
			if i not in notes_returned:
				notes_returned.append(i)
		if new_y_coord == i.coord_y:
			if i not in notes_returned:
				notes_returned.append(i)
		if new_text in i.message:
			if i not in notes_returned:
				notes_returned.append(i)
"""

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
serverPort = main_board.port_number

# Bind the socket to server address and server port
serverSocket.bind(("", int(serverPort)))

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

	# Perform function/command (POST/GET/PIN/UNDERPIN/CLEAR/DISCONNECT)
	server_response = main(string)

	# Send results back to client
	connectionSocket.send(server_response.encode())

	# End connection with client
	connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
