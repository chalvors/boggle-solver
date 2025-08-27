################################################
# Cole Halvorson
# detect.py
# detect a boggle board in an image
################################################

import cv2
import numpy as np
import math
import easyocr

class Detect:
     
    def __init__(self):
        self.board_cell_count = 16
        self.cells = [None] * self.board_cell_count
        self.reader = easyocr.Reader(['en'])
        self.letters = [None] * self.board_cell_count
        self.acc = [None] * self.board_cell_count


    # Edge detection and preprocessing
    def preprocess_image(self, image):

        print('Processing image')

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Sobel operator
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges
        
        # Compute gradient magnitude
        gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)
        
        # Convert to uint8
        gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

        _, binary_edges = cv2.threshold(gradient_magnitude, 50, 255, cv2.THRESH_BINARY)

        # A 40x40 square kernel
        kernel = np.ones((40, 40), np.uint8)

        # Perform the closing operation
        closed_edges = cv2.morphologyEx(binary_edges, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key=cv2.contourArea)

        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Crop the image based on the bounding box
        cropped_image = gray[y:y+h, x:x+w]

        # Resize and crop out margin
        image_size = 800
        margin = int(image_size * 0.1) # margin of 10%
        resized = cv2.resize(cropped_image, (image_size, image_size))
        no_margin = resized[margin:image_size-margin, margin:image_size-margin]

        return no_margin
    

    # Divide image into cells
    def divide_image(self, image):

        print('Dividing image')

        board_side_length = int(math.sqrt(self.board_cell_count))
        _, cropped_width = image.shape

        cell_size = int(cropped_width/board_side_length)
        cells = []

        # Rows
        for i in range(board_side_length):
            start_x = cell_size * i
            end_x = cell_size * (i + 1)

            # Cells in each row
            for j in range(board_side_length):

                start_y = cell_size * j
                end_y = cell_size * (j + 1)

                cell = image[start_x:end_x, start_y:end_y]
                cells.append(cell)

        return cells
    

    # Find errors
    def __update_errors(self):

        self.errors = []

        for index, num in enumerate(self.acc):

            # Add cell to errors if accuracy is less than 90%
            if (num < 0.90):
                self.errors.append(index + 1)

        
    # Read letters from cells 
    def __read_cells(self):
        output = []

        for img in self.cells:
            letter = self.reader.readtext(img)
            output.append(letter)

        for index, entry in enumerate(output):

            if(entry):
                self.letters[index] = entry[0][1]
                self.acc[index] = float(entry[0][2])
                
            else:
                self.letters[index] = ''
                self.acc[index] = 0
        
        self.__update_errors()


    # Rotate error cells for future reading
    def __rotate_error_cells(self):

        print('Rotating cells: ' + str(self.errors))

        for index, cell in enumerate(self.cells):
            for error in self.errors:

                # if cell is an error cell
                if (index == error-1):
                    
                    # Rotate 90 clockwise
                    new_cell = cv2.rotate(cell, cv2.ROTATE_90_CLOCKWISE)

                else:
                    new_cell = self.cells[index]

                self.cells[index] = new_cell


    # Replace remaining errors
    def __replace_errors(self): 

        print('')
        print('Replacing errors on cells: ' + str(self.errors))


        for index, letter in enumerate(self.letters):

            if letter == '':
                self.letters[index] = '?'
            elif letter == '0':
                self.letters[index] = 'O'
            elif letter == '1':
                self.letters[index] = 'I'
            elif letter == '2':
                self.letters[index] = 'Z'    
            elif letter == '3':
                self.letters[index] = 'E'
            elif letter == '4':
                self.letters[index] = 'A'
            elif letter == '5':
                self.letters[index] = 'S'
            elif letter == '6':
                self.letters[index] = '?'
            elif letter == '7':
                self.letters[index] = '?'            
            elif letter == '8':
                self.letters[index] = '?'
            elif letter == '9':
                self.letters[index] = '?'


    # Create board from letters
    def __create_board(self):

        board = []
        row = []

        for i in range(4):
            for j in range(4):
                row.append(self.letters[j + (4 * i)])
            
            board.append(row)
            row = []
        
        return board


    # Print boggle board
    def print_board(self, board):

        size = int(math.sqrt(self.board_cell_count))

        print('')
        print('Detected ' + str(size) + 'x' + str(size) + ' board:')
        print('')
        
        for row in board:
            print(row)

        print('')

    # Get letters from image
    def detect_letters(self, image):

        print('')
        print("Received image, detecting board")
        print('')

        # Process image
        processed_image = self.preprocess_image(image)

        # Divide image into cells
        self.cells = self.divide_image(processed_image)

        # Read cells
        self.__read_cells()

         # Rotate and read error cells 3 times
        for i in range(3):

            self.__rotate_error_cells()
            self.__read_cells()

        # Replace error cells
        self.__replace_errors()

        # Create and return board
        board = self.__create_board()
        return board