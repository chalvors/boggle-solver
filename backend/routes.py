from app import app
from flask import request, jsonify
import cv2
import numpy as np
import detect
import solve

# detect board
# input: image
# return: board matrix
@app.route('/api/detect', methods=['PUT'])
def detect_board():

    try:

        # pull image out of request
        file = request.files['image']
        file_bytes = np.fromfile(file, np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # detect board
        board = detect.detect_letters(image)
        board_size = len(board)
        detect.printBoard(board, board_size)

        return jsonify({"board": board})
    
    except Exception as e:
        return jsonify(str(e))
    

# solve board
# input: board matrix
# return: words array
@app.route('/api/solve', methods=['PUT'])
def solve_board():

    try:

        board = request.json
        board_size = len(board)

        words = solve.find_words(board, board_size)

        return jsonify({"words": words})
    
    except Exception as e:
        return jsonify(str(e))