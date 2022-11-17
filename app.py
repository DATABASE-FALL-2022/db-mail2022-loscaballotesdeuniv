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


@app.route('/users/creditcards', methods=['GET'])
def getAllUserCreditCards():
    return UserHandler().getAllUsersCreditCards()


@app.route('/users/emails/delete/<int:user_id>/<string:ename>', methods=['GET', 'DELETE'])
def getUserEmailsByIDENAME(user_id, ename):
    if request.method == 'GET':
        return UserHandler().getUserEmailsByIDENAME(user_id, ename)
    elif request.method == 'DELETE':
        return UserHandler().deleteEmail(user_id, ename)
    else:
        return jsonify(Error="Method not allowed."), 405




if __name__ == '__main__':
    app.run()
