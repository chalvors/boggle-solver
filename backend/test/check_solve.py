import sys
sys.path.insert(1, '../')
from solve import Solve

solve = Solve('../valid_words.json')
board = [
    ['T', 'U', 'R', 'N'], 
    ['A', 'A', 'S', 'I'], 
    ['E', 'P', 'I', 'U'], 
    ['B', 'E', 'A', 'R']
]
board_size = len(board)

found_words = solve.find_words(board, board_size)
print(found_words)