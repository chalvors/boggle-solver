################################################
# Cole Halvorson
# solve.py
# solve a given boggle board
# Credit: 
# - Geeks For Geeks Boggle Solver Tutorial
# - Github user benjamincrom word list
################################################

import json

class Solve:
     
    def __init__(self, valid_words_path):
        
        f = open(valid_words_path, 'r')
        self.valid_words = json.load(f)
        f.close()

        self.found = []


    # Recursive function to find all words present on boggle
    def __find_words_util(self, board, board_size, visited, i, j, current_string):

        # Mark current cell as visited and append current character to str
        visited[i][j] = True
        current_string = current_string + board[i][j]
        
        # If str is 3+ letters and is present in dictionary, add to found
        if (len(current_string) > 2):
            try:
                self.valid_words[current_string]
                self.found.append(current_string)
            except:
                pass
        
        # Traverse 8 adjacent cells of boggle[i,j]
        row = i - 1
        while row <= i + 1 and row < board_size:
            col = j - 1
            while col <= j + 1 and col < board_size:
                if (row >= 0 and col >= 0 and not visited[row][col]):
                    self.__find_words_util(board, board_size, visited, row, col, current_string)
                col+=1
            row+=1

        # Erase current character from string and mark visited of current cell as false
        current_string = "" + current_string[-1]
        visited[i][j] = False


    # Find all words present in dictionary.
    def find_words(self, board, board_size):

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
                self.__find_words_util(board, board_size, visited, i, j, Str)


        # Remove duplicates
        no_dupes = list(set(self.found))
        # Sort by alphabetical order, then by descending length
        sorted = no_dupes.sort(key=lambda word: (-len(word), word))

        num_words = str(len(sorted))
        print('Found ' + num_words + ' words')
        print('')

        return sorted