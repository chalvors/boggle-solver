from app import app
from flask import request, jsonify
import cv2
import numpy as np

from detect import Detect
from solve import Solve

# Detect board: image -> board matrix
@app.route('/api/detect', methods=['PUT'])
def detect_board():

    try:

        # Pull image out of request
        file = request.files['image']
        file_bytes = np.fromfile(file, np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Detect board
        detect = Detect()
        board = detect.detect_letters(image)
        detect.print_board(board)

        return jsonify({"board": board})
    
    except Exception as e:
        return jsonify(str(e))
    

# Solve board: board matrix -> words array
@app.route('/api/solve', methods=['PUT'])
def solve_board():

    try:

        board = request.json
        board_size = len(board)

        solve = Solve('./valid_words.json')
        words = solve.find_words(board, board_size)

        return jsonify({"words": words})
    
    except Exception as e:
        return jsonify(str(e))