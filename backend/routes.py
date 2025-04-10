from app import app, db
from flask import request, jsonify
from models import Friend


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

        data = request.json
        board = data["board"]

        print("SOLVE HERE")

        # solve board and return list of words

        return jsonify("received:", board)
    
    except Exception as e:
        return jsonify({"error:", str(e)})