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
        self.cell_images = []
        self.reader = easyocr.Reader(['en'])
        self.letters = []


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

        
    # Read letters from cells 
    def __read_cells(self):

        cell_image_sets = []  # 2d array of rotated cell images
        ocr_output_sets = []  # 2d array of ocr outputs for rotated cell images

        # Store each rotated image for each cell
        for cell_image in self.cell_images:

            cell_rotations = []

            cell_image_rotated_90 = cv2.rotate(cell_image, cv2.ROTATE_90_CLOCKWISE)
            cell_image_rotated_180 = cv2.rotate(cell_image, cv2.ROTATE_180)
            cell_image_rotated_270 = cv2.rotate(cell_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 90 degrees counterclockwise = 270 degrees clockwise

            cell_rotations.append(cell_image)
            cell_rotations.append(cell_image_rotated_90)
            cell_rotations.append(cell_image_rotated_180)
            cell_rotations.append(cell_image_rotated_270)

            cell_image_sets.append(cell_rotations)
        

        # Read each rotated image and store the ocr output
        for image_set in cell_image_sets:

            cell_ocr_outputs = []

            for image in image_set:

                ocr_output = self.reader.readtext(image, allowlist='0123456789ABCDEFGHJKLMNOPQRSTUVWXYZ')  # only allow numbers and uppercase letters

                if(ocr_output):
                    letter = ocr_output[0][1]
                    confidence = float(ocr_output[0][2])
                    
                else:
                    letter = '?'
                    confidence = 0

                cell_ocr_outputs.append((letter, confidence))

            ocr_output_sets.append(cell_ocr_outputs)
        

        # Remove ocr results where one cell contains multiple chars
        for cell_ocr_outputs in ocr_output_sets:
            
            for ocr_output in cell_ocr_outputs:

                letter = ocr_output[0]

                if (len(letter) > 1):
                    cell_ocr_outputs.remove(ocr_output)

        
        for cell_ocr_outputs in ocr_output_sets:
    
            # Pick the ocr output that has the highest confidence value for each cell
            highest_confidence_ocr_output = max(cell_ocr_outputs, key=lambda c: c[1])

            letter = highest_confidence_ocr_output[0]
            self.letters.append(letter)
              

    # Replace numbers with logical letters
    def __replace_numbers(self): 

        print('Replacing numbers')

        for index, letter in enumerate(self.letters):

            if letter == '0':
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

        # Divide image into individual cells
        self.cell_images = self.divide_image(processed_image)

        # Read cells
        self.__read_cells()

        # Replace any numbers
        self.__replace_numbers()

        # Create and return board
        board = self.__create_board()
        return board