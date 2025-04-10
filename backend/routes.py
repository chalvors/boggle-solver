from app import app, db
from flask import request, jsonify
from models import Friend
import cv2
import numpy as np


# get all friends
@app.route("/api/friends", methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)


# create a friend
@app.route("/api/friends", methods=['POST'])
def create_friend():
    return



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