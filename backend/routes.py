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
        board = detect.detectLetters(image)
        boardSize = len(board)
        detect.printBoard(board, boardSize)

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
        boardSize = len(board)

        words = solve.findWords(board, boardSize)

        return jsonify({"words": words})
    
    except Exception as e:
        return jsonify(str(e))