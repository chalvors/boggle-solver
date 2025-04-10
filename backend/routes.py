from app import app
from flask import request, jsonify
import cv2
import numpy as np


# solve boggle
@app.route('/api/solve', methods=['PUT'])
def solve():

    try:

        file = request.files['image']
        file_bytes = np.fromfile(file, np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        cv2.imshow('img', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # solve board and return list of words

        return jsonify("received")
    
    except Exception as e:
        return jsonify(str(e))