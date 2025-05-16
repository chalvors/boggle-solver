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

dictionary = {}
found = []

# initialize dictionary from json file
def initDictionary():

    global dictionary

    f = open('./dictionary.json', 'r')
    data = json.load(f)
    f.close()
    
    return data

# A recursive function to find all words present on boggle
def findWordsUtil(board, boardSize, visited, i, j, Str):

    # Mark current cell as visited and append current character to str
    visited[i][j] = True
    Str = Str + board[i][j]
    
    # If str is present in dictionary, add to found
    try:
        dictionary[Str]
        found.append(Str)
    except:
        pass
    
    # Traverse 8 adjacent cells of boggle[i,j]
    row = i - 1
    while row <= i + 1 and row < boardSize:
        col = j - 1
        while col <= j + 1 and col < boardSize:
            if (row >= 0 and col >= 0 and not visited[row][col]):
                findWordsUtil(board, boardSize, visited, row, col, Str)
            col+=1
        row+=1
    
    # Erase current character from string and mark visited of current cell as false
    Str = "" + Str[-1]
    visited[i][j] = False

# Find all words present in dictionary.
def findWords(board, boardSize):

    global found
    global dictionary

    dictionary = initDictionary()

    print('')
    print('finding words')
    print('')
  
    # Mark all characters as not visited
    visited = [[False for i in range(boardSize)] for j in range(boardSize)]
    
    # Initialize current string
    Str = ""
    
    # Consider every character and look for all words starting with this character
    for i in range(boardSize):
      for j in range(boardSize):
        findWordsUtil(board, boardSize, visited, i, j, Str)


    no_dupes = list(set(found))
    no_dupes.sort(key=len, reverse=True) 

    numWords = str(len(no_dupes))
    print('found ' + numWords + ' words')
    print('')

    return no_dupes