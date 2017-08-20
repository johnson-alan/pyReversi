from termcolor import colored
import numpy as np
import random
import sys

# view
board_row_header = '    a   b   c   d   e   f   g   h'
board_row_top = '---+---+---+---+---+---+---+---'
white_piece = colored('●', 'white')
white_legal_move = colored('●', 'white', attrs=['blink'])
black_piece = colored('●', 'blue')
black_legal_move = colored('●', 'blue', attrs=['blink'])
board_piece = {0: '   |', 1: ' ' + white_piece + ' |', 2: ' ' + black_piece + ' |'}

# board model - will be an (8, 8) numpy array
board = []

# player color global (never changed after opening selection of game)
human_player = 1
computer_player = 2

# move entry validation and input-to-model transformation dicts
valid_grid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
valid_grid_numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
valid_show_moves = ['show moves', 'show move', 'show', 'moves', 'showmoves', 'showmove']
letter_to_int = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# PRINT FUNCTIONS
def print_title():
	print(colored('\n\n      ___         ___                    ___         ___         ___                ' +
		' \n     /  /\       /  /\        ___       /  /\       /  /\       /  /\      ___      ' +
		' \n    /  /::\     /  /:/_      /__/\     /  /:/_     /  /::\     /  /:/_    /  /\     ' +
		' \n   /  /:/\:\   /  /:/ /\     \  \:\   /  /:/ /\   /  /:/\:\   /  /:/ /\  /  /:/     ' +
		' \n  /  /:/~/:/  /  /:/ /:/_     \  \:\ /  /:/ /:/_ /  /:/~/:/  /  /:/ /::\/__/::\     ' +
		' \n /__/:/ /:/__/__/:/ /:/ /\___  \__\:/__/:/ /:/ //__/:/ /:/__/__/:/ /:/\:\__\/\:\__  ' +
		' \n \  \:\/:::::\  \:\/:/ /:/__/\ |  |:\  \:\/:/ /:\  \:\/:::::\  \:\/:/~/:/  \  \:\/\\ ' +
		' \n  \  \::/~~~~ \  \::/ /:/\  \:\|  |:|\  \::/ /:/ \  \::/~~~~ \  \::/ /:/    \__\::/ ' +
		' \n   \  \:\      \  \:\/:/  \  \:\__|:| \  \:\/:/   \  \:\      \__\/ /:/     /__/:/  ' +
		' \n    \  \:\      \  \::/    \__\::::/   \  \::/     \  \:\       /__/:/      \__\/   ' +
		' \n     \__\/       \__\/         ~~~~     \__\/       \__\/       \__\/               \n \n' +
		' by allenhj \n \n Welcome to the game \n', 'green'))

# board that shows only existing moves
def print_board(board):

	# np.where returns 2 same-length numpy arrays of row, col indices
	score_white = len(np.where(board == 1)[0])
	score_black = len(np.where(board == 2)[0])

	print(colored(board_row_header, 'green'))
	print('  ' + colored('/' + board_row_top + '\\', 'blue'))
	for i in range(0, 8):
		row = colored(str(i+1), 'green') + colored(' |', 'blue')
		#row = colored(str(i), 'green') + colored(' |', 'blue')
		for j in range(0, 8):
			row += board_piece[int(board[i][j])]
		row = row[:-1] + colored('|', 'blue')
		if i == 2:
			row += colored('	Score | ', 'green') + 'White: ' + str(score_white)
		if i == 3:
			row += colored('	      | ', 'green') + colored('Black: ' + str(score_black), 'blue')
		print(row)
		if i != 7:
			print(colored('  +', 'blue') + board_row_top + colored('+', 'blue'))
	print('  ' + colored('\\' + board_row_top + '/', 'blue'))

# board showing the current player's legal moves
def print_possible_moves_board(board, legal_moves, color):
	print('\n Your legal moves: \n')
	print(colored(board_row_header, 'green'))
	print('  ' + colored('/' + board_row_top + '\\', 'blue'))
	# 0-8 for terminal display, 1-9 for debug
	for i in range(0, 8):
		row = colored(str(i+1), 'green') + colored(' |', 'blue')
		for j in range(0, 8):
			if (i, j) in legal_moves:
				row += ' ' + white_legal_move + ' |' if color == 'white' else ' ' + black_legal_move + ' |'
			else:
				row += board_piece[int(board[i][j])]
		row = row[:-1] + colored('|', 'blue')
		print(row)
		if i != 7:
			print(colored('  +', 'blue') + board_row_top + colored('+', 'blue'))
	print('  ' + colored('\\' + board_row_top + '/', 'blue'))

# GAME FUNCTIONS

# prepare a new game board
# set start positions
# print initial move
def prepare_new_game(board):
	global human_player
	global computer_player

	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=18, cols=85))
	print_title()

	# get player choice
	choice = input('Choose Black or White (Black goes first): ').lower()
	while choice != 'black' and choice != 'white':
		choice = input('Invalid entry. Choose Black or White (Black\n goes first): ').lower()
	if choice == 'white':
		human_player, computer_player = 1, 2
	else:
		human_player, computer_player = 2, 1

	# clear board from previous game
	board = np.zeros(shape=(8,8))

	# set start positions
	board[3][3] = human_player
	board[3][4] = computer_player
	board[4][3] = computer_player
	board[4][4] = human_player

	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=45, cols=85))

	print('\n The game has begun \n Starting Postions: \n')
	print_board(board)

	# initial turn

	if choice != 'black':
		white_legal_moves, black_legal_moves = get_legal_moves(board)
		board = take_computer_turn(board, (white_legal_moves, black_legal_moves))
		print('\n Computer move: \n')
		print_board(board)

	white_legal_moves, black_legal_moves = get_legal_moves(board)
	return board, white_legal_moves, black_legal_moves

# get user input, validate it is a valid grid value and a legal move
def take_human_turn(board, legal_moves):
	global human_player

	legal_moves_shown = False
	invalid_entry = False
	valid_entry_not_legal = False
	move_is_legal = False

	while move_is_legal == False:
		# showing possible moves
		if legal_moves_shown:
			if valid_entry_not_legal:
				move = input('\n Illegal move. Enter one of the legal move grid values: ').lower()
				valid_entry_not_legal = False
			elif invalid_entry:
				move = input('\n Invalid entry. Valid entries are in form `a2`, `g6`, (i.e. A-H, 1-8). Enter: ').lower()
				invalid_entry = False
			else:
				move = input('\n Choose a move by entering one of the legal move grid values: ').lower()

			valid_entry = (len(move) == 2 and move[0] in valid_grid_letters and move[1] in valid_grid_numbers)

			if valid_entry == False:
				invalid_entry = True
			else:
				grid_val = move_to_grid_val(move)
				if grid_val in (legal_moves[human_player-1]):
					move_is_legal = True
					board = update_board(board, grid_val, human_player)
				else:
					valid_entry_not_legal = True
		# not showing possible moves
		else:
			if valid_entry_not_legal:
				move = input('\n Illegal move. Enter one of the legal move grid\n values or `Show Moves` for a hint: ').lower()
				valid_entry_not_legal = False
			elif invalid_entry:
				move = input('\n Invalid entry. Valid entries are in form `a2`,\n `g6`, (i.e. A-H, 1-8) or `Show Moves`: ').lower()
				invalid_entry = False
			else:
				move = input('\n Choose a move by entering grid value, or enter\n `Show Moves` to see all legal moves: ').lower()

			valid_entry = (len(move) == 2 and move[0] in valid_grid_letters and move[1] in valid_grid_numbers or move in valid_show_moves)

			if valid_entry and move in valid_show_moves:
				legal_moves_shown = True
				print_possible_moves_board(board, legal_moves[human_player-1], 'white' if human_player == 1 else 'black')
			elif valid_entry == False:
				invalid_entry = True
			else:
				grid_val = move_to_grid_val(move)
				if grid_val in (legal_moves[human_player-1]):
					move_is_legal = True
					board = update_board(board, grid_val, human_player)
				else:
					valid_entry_not_legal = True

	return board

# choose a random move out of legal moves
# lots of room for expansion into Othello/Reversi AI algos in a v2
def take_computer_turn(board, legal_moves):
	# legal_moves is a tuple of white and black legal moves
	global computer_player

	print(computer_player)
	print(legal_moves)
	print(len(legal_moves))
	if len(legal_moves) == 2 :
		move = legal_moves[computer_player - 1][random.randint(0, len(legal_moves[computer_player - 1]) -1)]
	elif len(legal_moves == 1):
		# special case: no opponent moves list, in shape [(n,n)...] instead of [[(n,n)...], [(n,n)...]]
		move = legal_moves[0]
		print("IN NO MOVES SET")
	board = update_board(board, move, computer_player)
	return board

# print out the final score and declare a winner
def end_game(board):
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=15, cols=69))
	print(colored('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GAME OVER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'green',))
	score_white = len(np.where(board == 1)[0])
	score_black = len(np.where(board == 2)[0])
	line_one = ' ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ● '
	line_two = '   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   '
	if score_white > score_black:
		for i in range(0, 2):
			print(colored(line_one, 'white', attrs=['blink']))
			print(colored(line_two, 'white', attrs=['blink']))
		print(colored(' ●   ●   ●   ●   ●   ●   ●  ', 'white', attrs=['blink']) + \
			  'White Wins!' + colored('  ●   ●   ●   ●   ●   ●   ● ', 'white', attrs=['blink']))
		for i in range(0, 2):
			print(colored(line_two, 'white', attrs=['blink']))
			print(colored(line_one, 'white', attrs=['blink']))
	elif score_black > score_white:
		for i in range(0, 2):
			print(colored(line_one, 'blue', attrs=['blink']))
			print(colored(line_two, 'blue', attrs=['blink']))
		print(colored(' ●   ●   ●   ●   ●   ●   ●  ', 'blue', attrs=['blink']) + \
			  colored('Black Wins!', 'blue') + \
			  colored('  ●   ●   ●   ●   ●   ●   ● ', 'blue', attrs=['blink']))
		for i in range(0, 2):
			print(colored(line_two, 'blue', attrs=['blink']))
			print(colored(line_one, 'blue', attrs=['blink']))
	else:
		line_one = ' '
		line_two = '   '
		blue = colored('●   ', 'blue', attrs=['blink'])
		white = colored('●   ', 'white', attrs=['blink'])
		for i in range (0, 8):
			line_one += blue + white
			line_two += blue + white
		line_one += blue
		for i in range(0, 2):
			print(line_one)
			print(line_two)
		print(' ' + (blue + white) * 3 + colored('●   ', 'blue', attrs=['blink']) + \
			  colored('●  ', 'white', attrs=['blink']) + \
			  'Tie' + colored('  ●   ', 'white', attrs=['blink']) + \
			  colored('●   ', 'blue', attrs=['blink']) + ((white + blue) * 3))
		for i in range(0, 2):
			print(line_two)
			print(line_one)
	print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'green',))

# start a new game if player wants to play again
def play_again():
	choice = input('\n Play again (`yes`/`no`)?: ').lower()
	while choice not in ('yes', 'no', 'y', 'n', 'ye'):
		choice = input('\n Play again (`yes`/`no`?): ').lower()
	if choice[0] == 'y':
		board = []
		play_game(board)


# play game
def play_game(board):
	board, white_legal_moves, black_legal_moves = prepare_new_game(board)
	if white_legal_moves == False:
		white_legal_moves, black_legal_moves = get_legal_moves(board)
	while white_legal_moves and black_legal_moves:
		# human turn
		board = take_human_turn(board, (white_legal_moves, black_legal_moves))
		print('\n Your move: \n')
		print_board(board)

		# recompute legal moves
		white_legal_moves, black_legal_moves = get_legal_moves(board)

		# computer turn
		if white_legal_moves and black_legal_moves:
			board = take_computer_turn(board, (white_legal_moves, black_legal_moves))
			print('\n Computer move: \n')
			print_board(board)

			# recompute legal moves
			white_legal_moves, black_legal_moves = get_legal_moves(board)

	end_game(board)
	play_again()


# HELPER FUNCTIONS

# determine legal moves for both players
def get_legal_moves(board):
	white_pieces = np.where(board == 1)
	black_pieces = np.where(board == 2)

	white_legal_moves = []
	black_legal_moves = []

	for color in [('white', white_pieces), ('black', black_pieces)]:
		pieces = color[1]
		player = 1 if color[0] == 'white' else 2
		opponent = 2 if color[0] == 'white' else 1
		legal_moves = []

		# numpy where() result is two np arrays of row and column indices of matches
		for piece in zip(pieces[0], pieces[1]):
			row = piece[0]
			col = piece[1]

			# get the box of values surrounding a cell
			rect = get_rect(board, row, col)

			# get positions in rect that have enemy moves (directions to explore)
			# this way we don't have to check 8 possible move directions for every piece every time!
			opponent_pieces = np.where(rect == opponent)

			for move in zip(opponent_pieces[0], opponent_pieces[1]):
				# normalize 0 to 2 into -1 to 1 to get direction vector
				y_direction = move[0] - 1
				x_direction = move[1] - 1

				# to start, move in vector direction two steps (over the opponent piece we just identified)
				new_row = row + y_direction * 2
				new_col = col + x_direction * 2

				#  if cell is empty, stop and add to legal moves
				#  if piece in cell is your own, stop
				#  if piece in cell is opponent's, continue
				#  continue moving one step in direction until empty cell or end of board
				while new_row >= 0 and new_row <= 7 and new_col >= 0 and new_col <= 7:
					if board[new_row][new_col] == 0:
						# don't add twice if it's already there from another piece's legal moveset
						if (new_row, new_col) not in legal_moves:
							legal_moves.append((new_row, new_col))
						break
					elif board[new_row][new_col] == opponent:
						new_row += y_direction
						new_col += x_direction
					else:
						# own piece
						break

		if player == 1:
			white_legal_moves = legal_moves
		else:
			black_legal_moves = legal_moves

	return white_legal_moves, black_legal_moves

# update the board based on the selected move
def update_board(board, grid_val, player):
	opponent = 2 if player == 1 else 1

	row = grid_val[0]
	col = grid_val[1]

	# simpler variant of get_legal_moves() algo
	rect = get_rect(board, row, col)
	opponent_pieces = np.where(rect == opponent)

	for move in zip(opponent_pieces[0], opponent_pieces[1]):
		# normalize 0 to 2 into -1 to 1 to get direction vector
		y_direction = move[0] - 1
		x_direction = move[1] - 1

		# skip over piece we know is opponent's
		new_row = row + y_direction * 2
		new_col = col + x_direction * 2

		# add initial opponent piece
		pieces_to_flip = [(row, col), (row + y_direction, col + x_direction)]

		#  if cell is empty, stop
		#  if piece in cell is opponent's, add to pieces_to_flip list continue
		#  if piece in cell is your own, stop and flip pieces in pieces_to_flip
		#  continue moving one step in direction until above case or end of board
		while (new_row >= 0 and new_row <= 7 and new_col >= 0 and new_col <= 7):
			if board[new_row][new_col] == opponent:
				pieces_to_flip.append((new_row, new_col))
				new_row += y_direction
				new_col += x_direction
			elif board[new_row][new_col] == player:
				for piece in pieces_to_flip:
					board[piece[0]][piece[1]] = player
				break
			else:
				# empty cell
				break

	return board

# change player input to numpy-readable row,col
def move_to_grid_val(move):
	col = int(letter_to_int[move[0]])
	row = int(move[1])-1
	return (row, col)

# return a square window of pieces adjacent to the selected move
def get_rect(board, row, col):
	# special cases that limit a moveset:
	# 	all of rows 0, 7 and all of cols 0, 7, excluding corners
	# 	corners = (0,0), (0,7), (7,0), (7, 7)
	# default: any interior cell (neither row nor col is 0 or 7)
	#
	# - must be converted into a 3x3 np array to preserve direction
	# 	vector functionality
	# - check most common to least common case for compute efficiency
	#

	if row > 0 and row < 7 and col > 0 and col < 7:
		# get immediate square around the piece
		rect = np.reshape([board[i][j] for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)], (3,3))
		return rect
	elif row == 0 and col not in (0, 7):
		# top-edge rect
		rect = np.reshape([board[i][j] for i in range(row, row + 2) for j in range(col-1, col + 2)], (2,3))
		rect = np.concatenate((np.array([[0.,0.,0.]]), rect))
		return rect
	elif row == 7 and col not in (0, 7):
		# bottom-edge rect
		rect = np.reshape([board[i][j] for i in range(row - 1, row + 1) for j in range(col-1, col + 2)], (2,3))
		rect = np.concatenate((rect, np.array([[0.,0.,0.]])))
		return rect
	elif col == 0 and row not in (0, 7):
		# left-edge rect
		rect = np.reshape([board[i][j] for i in range(row - 1, row + 2) for j in range(col, col + 2)], (3,2))
		rect = np.concatenate((np.array([[0.,0.,0.]]).T, rect), axis=1)
		return rect
	elif col == 7 and row not in (0, 7):
		# right-edge rect
		rect = np.reshape([board[i][j] for i in range(row - 1, row + 2) for j in range(col-1, col + 1)], (3,2))
		rect = np.concatenate((rect, np.array([[0.,0.,0.]]).T), axis=1)
		return rect
	else:
		# corner: (0,0), (0,7), (7,0), (7,7)):
		if row == 0 and col == 0:
			rect = np.reshape([board[i][j] for i in range(row, row + 2) for j in range(col, col + 2)], (2,2))
			rect = np.pad(rect, pad_width=((1,0), (1,0)), mode='constant', constant_values=0)
		elif row == 0 and col == 7:
			rect = np.reshape([board[i][j] for i in range(row, row + 2) for j in range(col - 1, col + 1)], (2,2))
			rect = np.pad(rect, pad_width=((1,0), (0,1)), mode='constant', constant_values=0)
		elif row == 7 and col == 0:
			rect = np.reshape([board[i][j] for i in range(row - 1, row + 1) for j in range(col, col + 2)], (2,2))
			rect = np.pad(rect, pad_width=((0,1), (1,0)), mode='constant', constant_values=0)
		elif row == 7 and col == 7:
			rect = np.reshape([board[i][j] for i in range(row - 1, row + 1) for j in range(col - 1, col + 1)], (2,2))
			rect = np.pad(rect, pad_width=((0,1), (0,1)), mode='constant', constant_values=0)
	return rect

# MAIN
play_game(board)
