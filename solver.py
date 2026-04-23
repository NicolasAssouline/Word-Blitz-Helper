import logging
from typing import List

from env import LOG_LEVEL
from utils import load_dictionary

logger = logging.getLogger(__name__)


_VALID_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def _in_bounds(board, x, y):
	return 0 <= x < len(board) and 0 <= y < len(board[x])

def find_word_in_board(board, word, visited=None):
	if visited is None:
		if len(word) == 0:
			raise ValueError('The length of the word must be greater than zero')

		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] == word[0]:
					path = find_word_in_board(board, word[1:], [(i, j)])
					if path is not None:
						return path
		return None  # the word cannot be found on the board
	elif len(word) == 0:  # recursion finished
		return visited

	curr_x, curr_y = visited[-1]
	for dx, dy in _VALID_DIRECTIONS:
		new_x, new_y = curr_x + dx, curr_y + dy
		if _in_bounds(board, new_x, new_y) and board[new_x][new_y] == word[0] and (new_x, new_y) not in visited:
			visited.append((new_x, new_y))
			return find_word_in_board(board, word[1:], visited.copy())
	return None


def solve_blitz(board: List[List[str]], word_dictionary: set=None):
	if word_dictionary is None:
		word_dictionary = load_dictionary()
	word_dictionary = {word.upper() for word in word_dictionary}

	letters_in_board = set(item for sublist in board for item in sublist)

	# pre-filter the dictionary to the set of all possible words
	words_in_board = filter(lambda entry: all(letter in letters_in_board for letter in entry), word_dictionary)

	logger.info('Words present on the board:')

	words_found = 0
	paths = []
	for word in sorted(words_in_board, key=len):
		path = find_word_in_board(board, word)
		if path is None:
			continue

		words_found += 1
		logger.info(f'{word:17} path = {path}')
		paths.append(path)

	logger.info(f'Words found: {words_found}')
	return paths

# test
if __name__ == '__main__':
	logging.basicConfig(level=LOG_LEVEL)
	example_board = [
		['O', 'V', 'A', 'O'],
		['R', 'U', 'D', 'V'],
		['O', 'V', 'T', 'O'],
		['R', 'E', 'G', 'K']
	]

	solve_blitz(example_board)