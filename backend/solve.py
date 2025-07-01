################################################
# Cole Halvorson
# CS455 Final Project
# 11/22/2024
#
# solve.py
# solve a given boggle board
#
# Credit: 
# - Geeks For Geeks Boggle Solver Tutorial
# - Github user benjamincrom word list
################################################

import json

f = open('./valid_words.json', 'r')
valid_words = json.load(f)
f.close()

found = []

# A recursive function to find all words present on boggle
def find_words_util(board, board_size, visited, i, j, current_string):

    # Mark current cell as visited and append current character to str
    visited[i][j] = True
    current_string = current_string + board[i][j]
    
    # If str is 3+ letters and is present in dictionary, add to found
    if (len(current_string) > 2):
        try:
            valid_words[current_string]
            found.append(current_string)
        except:
            pass
    
    # Traverse 8 adjacent cells of boggle[i,j]
    row = i - 1
    while row <= i + 1 and row < board_size:
        col = j - 1
        while col <= j + 1 and col < board_size:
            if (row >= 0 and col >= 0 and not visited[row][col]):
                find_words_util(board, board_size, visited, row, col, current_string)
            col+=1
        row+=1
    
    # Erase current character from string and mark visited of current cell as false
    current_string = "" + current_string[-1]
    visited[i][j] = False

# Find all words present in dictionary.
def find_words(board, board_size):

    global found

    print('')
    print('Finding words')
    print('')
  
    # Mark all characters as not visited
    visited = [[False for i in range(board_size)] for j in range(board_size)]
    
    # Initialize current string
    Str = ""
    
    # Consider every character and look for all words starting with this character
    for i in range(board_size):
      for j in range(board_size):
        find_words_util(board, board_size, visited, i, j, Str)


    no_dupes = list(set(found))
    no_dupes.sort(key=len, reverse=True) 

    num_words = str(len(no_dupes))
    print('Found ' + num_words + ' words')
    print('')

    return no_dupes