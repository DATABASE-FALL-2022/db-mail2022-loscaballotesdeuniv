from flask import Flask, jsonify, request, send_file
from Handler.User import UserHandler

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def greeting():
    return "Los Caballotes de la Universidad"


@app.route('/users', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        return UserHandler().addNewUserJson(request.json)
    elif request.method == 'GET':
        return UserHandler().getAllUsers()

@app.route('/users/emails', methods=['GET'])
def getAllUserEmails():
    return UserHandler().getAllUsersEmails()

@app.route('/users/folders', methods=['GET'])
def getAllFolders():
    return UserHandler().getAllFolders()



@app.route('/users/emails/delete/<int:user_id>/<string:ename>', methods=['GET', 'DELETE'])
def getUserEmailsByIDENAME(user_id, ename):
    if request.method == 'GET':
        return UserHandler().getUserEmailsByIDENAME(user_id, ename)
    elif request.method == 'DELETE':
        return UserHandler().deleteEmail(user_id, ename)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/users/friends/<int:friend_id>', methods=['GET'])
def manage_friends(friend_id):
    if request.method == 'GET':
        return UserHandler().getAllUserFriends(friend_id)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/users/friends', methods=['POST'])
def addNewFriend():
    if request.method == 'POST':
        return UserHandler().addNewFriendByFriendID(request.json)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/users/<int:user_id>/friends/<int:friend_id>/delete', methods=['DELETE'])
def deleteFriendByFriendID(user_id, friend_id):
    if request.method == 'DELETE':
        return UserHandler().deleteFriendByFriendID(user_id, friend_id)
    else:
        return jsonify(Error="Method not allowed."), 405

if __name__ == '__main__':
    app.run()


