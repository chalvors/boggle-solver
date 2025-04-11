################################################
# Cole Halvorson
# CS455 Final Project
# 11/22/2024
#
# detect.py
# detect a boggle board in an image
################################################

import cv2
import easyocr

# Make reader
reader = easyocr.Reader(['en'])

# Globals
cells = [None] * 16
letters = [None] * 16
acc = [None] * 16
errors = []

def preprocessImage(image):

    print('Processing Image')

    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (800,800))

    # Crop out border
    resized_height, resized_width = resized.shape
    crop_margin = 70

    cropped = resized[crop_margin:resized_height-crop_margin, crop_margin:resized_width-crop_margin]

    return cropped

# Divide image into cells
# TODO this is bad
def divideImage(image):

    print('Dividing Image')

    cropped_height, cropped_width = image.shape

    divide_size = int(cropped_width/4)

    cell_1 = image[0:divide_size, 0:divide_size]
    cell_2 = image[0:divide_size, divide_size:divide_size*2]
    cell_3 = image[0:divide_size, divide_size*2:divide_size*3]
    cell_4 = image[0:divide_size, divide_size*3:divide_size*4]

    cell_5 = image[divide_size:divide_size*2, 0:divide_size]
    cell_6 = image[divide_size:divide_size*2, divide_size:divide_size*2]
    cell_7 = image[divide_size:divide_size*2, divide_size*2:divide_size*3]
    cell_8 = image[divide_size:divide_size*2, divide_size*3:divide_size*4]

    cell_9 = image[divide_size*2:divide_size*3, 0:divide_size]
    cell_10 = image[divide_size*2:divide_size*3, divide_size:divide_size*2]
    cell_11 = image[divide_size*2:divide_size*3, divide_size*2:divide_size*3]
    cell_12 = image[divide_size*2:divide_size*3, divide_size*3:divide_size*4]

    cell_13 = image[divide_size*3:divide_size*4, 0:divide_size]
    cell_14 = image[divide_size*3:divide_size*4, divide_size:divide_size*2]
    cell_15 = image[divide_size*3:divide_size*4, divide_size*2:divide_size*3]
    cell_16 = image[divide_size*3:divide_size*4, divide_size*3:divide_size*4]

    return(
        [
            cell_1, cell_2, cell_3, cell_4,
            cell_5, cell_6, cell_7, cell_8,
            cell_9, cell_10, cell_11, cell_12,
            cell_13, cell_14, cell_15, cell_16,
        ]
    )

# Find errors
def updateErrors():

    global errors
    errors = []

    for index, num in enumerate(acc):

        # Add cell to errors if accuracy is less than 90%
        if (num < 0.90):
            errors.append(index + 1)

# Read cells 
def readCells():

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
    
    updateErrors()

# Rotate error cells for future reading
def rotateErrorCells():

    print('rotating cells: ' + str(errors))

    global cells

    for index, cell in enumerate(cells):
        for error in errors:

            # if cell is an error cell
            if (index == error-1):
                
                # Rotate 90 clockwise
                newCell = cv2.rotate(cell, cv2.ROTATE_90_CLOCKWISE)

            else:
                newCell = cells[index]

            cells[index] = newCell

# Adjust errors
def replaceErrors(): 

    print('')
    print('error on cells: ' + str(errors))

    global letters

    for index, letter in enumerate(letters):

        if letter == '':
            letters[index] = ''
        elif letter == '3':
            letters[index] = 'E'
        elif letter == '5':
            letters[index] = 'S'
        elif letter == '1':
            letters[index] = 'I'
        elif letter == '0':
            letters[index] = 'O'
        elif letter == '4':
            letters[index] = 'A'

# Create board from letters
def createBoard():

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
def printBoard(board, size):

    print('')
    print('Detected ' + str(size) + 'x' + str(size) + ' board:')
    print('')
    
    for row in board:
        print(row)

    print('')
    

# Get letters from image
def detectLetters(image):

    print('')
    print("Received image, detecting board")
    print('')

    # Process image
    processedImage = preprocessImage(image)

    # Divide image into cells
    global cells
    cells = divideImage(processedImage)

    print('')

    # Read cells
    readCells()

    # Rotate and read error cells 3 times
    for i in range(3):

        rotateErrorCells()
        readCells()

    # Replace error cells
    replaceErrors()

    # Create and return board
    board = createBoard()
    return board