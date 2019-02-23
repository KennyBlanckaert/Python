# Functions
def display(board):
	print('   |   |   ')
	print(" " + board[0] + " | " + board[1] + " | " + board[2])
	print('---|---|---')
	print(" " + board[3] + " | " + board[4] + " | " + board[5])
	print('---|---|---')
	print(" " + board[6] + " | " + board[7] + " | " + board[8])
	print('   |   |   ')

def place_move_if_valid(board, player, position):
	if (board[position] == ' '):
		board[position] = player
		return True
	else:
		return False

def board_is_full(board):
	for square in board:
		if (square == " "):
			return False
	else:
		return True

def check_for_winner(board):
	if (board[0] == board[1] == board[2] != " " or board[3] == board[4] == board[5] != " " or board[6] == board[7] == board[8] != " "
		or board[0] == board[3] == board[6] != " " or board[1] == board[4] == board[7] != " " or board[2] == board[5] == board[8] != " "
		or board[0] == board[4] == board[8] != " " or board[2] == board[4] == board[6] != " "):
		return True
	else:
		return False
	

# Gameplay
print("Welcome at TicTacToe!")
print("This game uses a numeric keypad.")
print(" ")

turn = 0
players = ("X", "O")
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

display(board)
while(not board_is_full(board)):

	# Next turn
	position = int(input(f"(Player {players[turn]}) Enter the number of your chosen position: "))
	result = place_move_if_valid(board, players[turn], position - 1)

	# Display changes
	display(board)

	# Check board
	if (check_for_winner(board)):
		break

	# Move forward
	if (result):
		turn = (turn + 1) % 2
	else:
		print("That position has already been taken! Try again.")
		continue

if (check_for_winner(board)):
	print(f"############ Congratulations Player {players[turn]} ############")
else:
	print("############ DRAW ############")
