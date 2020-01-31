# Import socket module
from socket import * 
# Import for multithreading
import _thread
import threading
# Import to terminate the program
import sys 
colors = []
# Intial board
port_number = sys.argv[1]
board_width  = sys.argv[2]
board_height = sys.argv[3]

# Add colors
for x in sys.argv[4:]:
	colors.append(x)

for x in colors:
	print("Color added: " + str(x))

# Board class 
class board:
	# Initialzie board
	def __init__(self, port_number, board_width, board_height, colors):
		self.port_number = port_number
		self.board_width = board_width
		self.board_height = board_height
		self.colors = colors

# This is shared between all clients (share object)
main_board = board(port_number, board_width, board_height, colors)
# Data structure to hold note objects
notes = []
# Data structure to hold pin coordinates
pins = []

# Main function to call on other functions
def main(string):
	# Split string to get user request
	arr = string.split(" ", 1)
	# POST
	if arr[0].upper() == 'POST':
		# Split strinf to get each element
		arr = string.split(" ", 6)
		new_note = note(arr[1], arr[2], arr[3], arr[4], arr[5], arr[6])
		return post(new_note)
	# GET
	elif arr[0].upper() == 'GET':
		return get(string)
	# CLEAR
	elif arr[0].upper() == 'CLEAR':
		return clear()
	# PIN/UNPIN
	elif arr[0].upper() == 'PIN' or arr[0].upper() == 'UNPIN':
		# Split strinf to get each element
		arr = string.split(" ", 3)
		return pin(arr[0], arr[1], arr[2])
	# DISCONNECT
	elif arr[0].upper() == 'DISCONNECT':
		# Send some kind of message to client that server is closed
		disconnect()

# Note class 
class note:
	# Initialzie note 
	def __init__(self, coord_x, coord_y, width, height, color, message):
		self.coord_x = coord_x 	# X-Cord
		self.coord_y = coord_y	# Y-Cord
		self.width = width		# Width
		self.height = height	# Height
		self.color = color		# Color
		self.message = message	# Text 
		self.status = 0			# PINED/UNPINED indicator
	
	# Comparing
	def __eq__(self, other):
		if self.coord_x == other.coord_x and self.coord_y == self.coord_y \
		and self.width==other.width and self.height == other.height \
		and self.color == other.color and self.message == other.message:
			return True
		else:
			 return False

	# Retrun object in string form
	def __str__(self):
		return f'{self.coord_x} {self.coord_y} {self.width} {self.height} {self.color} {self.message}'

	# Check if the note will fit on the board
	def check_dimensions(self):
		if (int(self.coord_x) + int(self.width)) > int(main_board.board_width) or \
			(int(self.coord_y) + int(self.height)) > int(main_board.board_height):
			return False
		else:
			return True

	def check_color(self):
		if (self.color not in main_board.colors):
			return False
		else:
			return True

# Post incomplete - Must account for board information (color)
def post(note_obj):
	"""
	if (int(note_obj.height) + int(note_obj.coord_y)) < int(main_board.board_height) and \
		(int(note_obj.width) + int(note_obj.coord_x))<main_board.board_width:
		
		return "Message Posted" + str(note_obj.message)
		"""
	if (note_obj.check_dimensions() and note_obj.check_color()):
		notes.append(note_obj)
		return "note posted"
	elif(note_obj.check_dimensions() == False):
		return "Message not posted: Insufficient space on board"
	else:
		return "Message not posted: Color not permitted on board"
	# print("note posted: " + note_obj.message)


# GET function - retrives note from data strcture
def get(string):
	# Getting commands from client input
	command = string.replace("="," ").split()

	try:
		pin_index = command.index("PINS")
	except:
		pin_index = -1

	if (pin_index == -1):
		
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

		# Set new variables as either empty string or string parameter values
		if color_index != -1:
			new_color = command[color_index+1]
		else:
			new_color = ""
		if  contain_index != -1:
			new_x_coord = command[contain_index+1]
			new_y_coord = command[contain_index+2]
		else:
			new_x_coord = ""
			new_y_coord = ""
		if refers_index != -1:
			new_reference = command[refers_index+1:]
			new_text = ' '.join(new_reference)
		else:
			new_text = ""

		# copy the list to temp list
		notes_returned = notes.copy()

		# Filtering temp list based on client provided parameters
		j = 0
		while (j < len(notes_returned)):
			if (color_index != -1 and str(notes_returned[j].color) != str(new_color)):
				print("color popped: " + str(notes_returned[j].message))
				notes_returned.pop(j)
			elif (contain_index != -1 and (is_contained(notes_returned[j], new_x_coord, new_y_coord) == False)):
				print("contains popped: " + str(notes_returned[j].message))
				notes_returned.pop(j)
			elif (refers_index != -1 and str(new_text) not in str(notes_returned[j].message)):
				print("new_text is: " + str(new_text))
				print("refersTo popped: " + str(notes_returned[j].message))
				notes_returned.pop(j)
			else:
				j += 1

		# send messages to client
		obj_string = "\n"
		for x in notes_returned:
			if (x.status == 0):
				obj_string += str(x) + " - Unpinned\n"
			else:
				obj_string += str(x) + " - Pinned \n"
		return obj_string

	# PIN Command
	else:
		pin_string = "\n"
		for x in pins:
			pin_string += "PIN " + str(x[1]) + str(x[0]) + "\n"
		return pin_string

# CLEAR function - clears all UNPINED notes
def clear():
	i = 0;
	while (i < len(notes)):
		print("Status Of: " + str(notes[i].message) + " Is " + str(notes[i].status))
		if (notes[i].status <= 0):
			# print("Note removed: " + str(i.message))
			notes.pop(i)	# Remove note from list
		else:
			i += 1
	# Return message
	return "All Unpined Notes Cleared!"

# PIN function - updates the status of the note object 	
def pin(choice, x, y):
	for i in notes:
		# If pin lands on note
		if (is_contained(i, x, y) == True):
			print("pin is contained\n")
			if (choice == "PIN"):
				i.status += 1
				tup = (int(x), int(y))
				pins.append(tup)
				"""
				for j in pins:
					print("PIN " + str(j[0]) + " " + str(j[1]))
				"""
				return ("Note Pinned successfully at coord: " + str(j[0]) + " " + str(j[1]) + "\n")
			elif (choice == "UNPIN"):
				i.status -= 1
				return ("Note Unpinned successfully\n")
	return "No notes to pin\n"

# Function to determine if note can be pinned
def is_contained(note, x, y):
	if ((int(y)<(int(note.coord_y) + int(note.height)) and (int(y) > int(note.coord_y))) and \
		(int(x)<(int(note.coord_x) + int(note.width)) and (int(x) > int(note.coord_x)))):
		print("Note Not Contained")
		return True
	else:
		print("Note Contained")
		return False

# DISCONNECT function - server will disconnect from client
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
# Terminate the program after sending the corresponding data
sys.exit()