################################################
# Cole Halvorson
# detect.py
# detect a boggle board in an image
################################################

import cv2
import easyocr
import math

# Make reader
reader = easyocr.Reader(['en'])

# Globals
board_cell_count = 16
cells = [None] * board_cell_count
letters = [None] * board_cell_count
acc = [None] * board_cell_count
errors = []

def preprocess_image(image):

    print('Processing image')

    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (800,800))

    # Crop out border
    resized_height, resized_width = resized.shape
    crop_margin = 70

    cropped = resized[crop_margin:resized_height-crop_margin, crop_margin:resized_width-crop_margin]

    return cropped

# Divide image into cells
def divide_image(image):

    print('Dividing image')

    board_side_length = int(math.sqrt(board_cell_count))
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
def update_errors():

    global errors
    errors = []

    for index, num in enumerate(acc):

        # Add cell to errors if accuracy is less than 90%
        if (num < 0.90):
            errors.append(index + 1)

# Read cells 
def read_cells():

    global cells
    global letters
    global acc

    output = []

    for img in cells:
        letter = reader.readtext(img)
        output.append(letter)

    for index, entry in enumerate(output):

        if(entry):
            letters[index] = entry[0][1]
            acc[index] = float(entry[0][2])
            
        else:
            letters[index] = ''
            acc[index] = 0
    
    update_errors()

# Rotate error cells for future reading
def rotate_error_cells():

    print('Rotating cells: ' + str(errors))

    global cells

    for index, cell in enumerate(cells):
        for error in errors:

            # if cell is an error cell
            if (index == error-1):
                
                # Rotate 90 clockwise
                new_cell = cv2.rotate(cell, cv2.ROTATE_90_CLOCKWISE)

            else:
                new_cell = cells[index]

            cells[index] = new_cell

# Adjust errors
def replace_errors(): 

    print('')
    print('Error on cells: ' + str(errors))

    global letters

    for index, letter in enumerate(letters):

        if letter == '':
            letters[index] = '?'
        elif letter == '0':
            letters[index] = 'O'
        elif letter == '1':
            letters[index] = 'I'
        elif letter == '2':
            letters[index] = 'Z'    
        elif letter == '3':
            letters[index] = 'E'
        elif letter == '4':
            letters[index] = 'A'
        elif letter == '5':
            letters[index] = 'S'
        elif letter == '6':
            letters[index] = '?'
        elif letter == '7':
            letters[index] = '?'            
        elif letter == '8':
            letters[index] = '?'
        elif letter == '9':
            letters[index] = '?'

# Create board from letters
def create_board():

    global letters

    board = []
    row = []

    for i in range(4):
        for j in range(4):
            row.append(letters[j + (4 * i)])
        
        board.append(row)
        row = []
    
    return board


# Print boggle board
def print_board(board, size):

    print('')
    print('Detected ' + str(size) + 'x' + str(size) + ' board:')
    print('')
    
    for row in board:
        print(row)

    print('')
    

# Get letters from image
def detect_letters(image):

    print('')
    print("Received image, detecting board")
    print('')

    # Process image
    processedImage = preprocess_image(image)

    # Divide image into cells
    global cells
    cells = divide_image(processedImage)

    print('')

    # Read cells
    read_cells()

    # Rotate and read error cells 3 times
    for i in range(3):

        rotate_error_cells()
        read_cells()

    # Replace error cells
    replace_errors()

    # Create and return board
    board = create_board()
    return board