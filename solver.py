from typing import List

from utils import load_dictionary


def find_word_in_board(board, word, curr_pos=None, visited=None):

	# depth 1 in the recursion
	if visited is None and curr_pos is None:
		if len(word) == 0: raise ValueError('The length of the word must be greater than zero')

		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] == word[0]:
					path = find_word_in_board(board, word[1:], (i, j), [(i, j)])
					if path is not None:
						return path
		return None # the word cannot be found on the board
	elif len(word) == 0: # recursion finished
		return visited

	curr_x, curr_y = curr_pos
	for i in range(max(0, curr_x-1), min(3, curr_x+1)+1):
		for j in range(max(0, curr_y-1), min(3, curr_y+1)+1):
			if board[i][j] == word[0] and (i, j) not in visited:
				visited.append((i, j))
				return find_word_in_board(board, word[1:], (i, j), visited.copy())
	return None


def solve_blitz(board: List[List[str]], word_dictionary:set=None):
	if word_dictionary is None:
		word_dictionary = load_dictionary()
	word_dictionary = [word.upper() for word in word_dictionary]

	letters_in_board = set([item for sublist in board for item in sublist])

	# pre-filter the dictionary to the set of all possible words
	word_dictionary = list(filter(lambda entry: all([letter in letters_in_board for letter in entry]), word_dictionary))

	print('Words found in board')
	for word in sorted(word_dictionary, key=len):
		path = find_word_in_board(board, word)

		if path is not None:
			print(word, '\tpath =', path)

	print('\nScan complete')

if __name__ == '__main__':
	board = [
		['O', 'V', 'A', 'O'],
		['R', 'U', 'D', 'V'],
		['O', 'V', 'T', 'O'],
		['R', 'E', 'G', 'K']
	]

	solve_blitz(board)