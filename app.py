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

if __name__ == '__main__':
    app.run()
