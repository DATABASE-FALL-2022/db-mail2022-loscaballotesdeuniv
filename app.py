from flask import Flask, jsonify, request, send_file

from Handler.User import UserHandler
from Handler.Folder import FolderHandler
from Handler.Email import EmailHandler
from Handler.CreditCard import CreditCardHandler

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/loscaballotesdeuniv')
def greeting():
    return "Los Caballotes de la Universidad Present RUMail Services"


@app.route('/loscaballotesdeuniv/users', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        return UserHandler().addNewUserJson(request.json)
    elif request.method == 'GET':
        return UserHandler().getAllUsers()

@app.route('/loscaballotesdeuniv/users/<int:user_id>', methods=['GET'])
def getUsersByID(user_id):
   return UserHandler().getUsersByID(user_id)

@app.route('/loscaballotesdeuniv/users/<int:user_id>/folders', methods=['GET'])
def getUsersFoldersByID(user_id):
   return FolderHandler().getUsersFolderByID(user_id)

@app.route('/loscaballotesdeuniv/users/<int:user_id>/email', methods=['GET'])
def getUserEmailByID(user_id):
   return UserHandler().getUserEmailByID(user_id)


@app.route('/loscaballotesdeuniv/users/<int:user_id>/all/emails', methods=['GET'])
def getAllUsersEmailsByID(user_id):
   return EmailHandler().getAllUsersEmailsByID(user_id)

@app.route('/loscaballotesdeuniv/users/<int:user_id>/creditcard', methods=['GET'])
def getUsersCreditCardByID(user_id):
   return CreditCardHandler().getUsersCreditCardByID(user_id)

@app.route('/loscaballotesdeuniv/emails', methods=['GET', 'POST'])
def getAllUserEmails():
    if request.method == 'GET':
        return EmailHandler().getAllUsersEmails()
    elif request.method == 'POST':
        return EmailHandler().createEmailJson(request.json)

@app.route('/loscaballotesdeuniv/folders', methods=['GET'])
def getAllFolders():
    return FolderHandler().getAllFolders()


@app.route('/loscaballotesdeuniv/creditcards', methods=['GET'])
def getAllUserCreditCards():
    return CreditCardHandler().getAllUsersCreditCards()


@app.route('/loscaballotesdeuniv/users/emails/<int:user_id>/<string:ename>', methods=['GET', 'DELETE'])
def getUserEmailsByIDENAME(user_id, ename):
    if request.method == 'GET':
        return EmailHandler().getUserEmailsByIDENAME(user_id, ename)
    elif request.method == 'DELETE':
        return EmailHandler().deleteEmail(user_id, ename)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/loscaballotesdeuniv/users/friends/<int:friend_id>', methods=['GET'])
def manage_friends(friend_id):
        if request.method == 'GET':
            return UserHandler().getAllUserFriends(friend_id)
        else:
            return jsonify(Error="Method not allowed."), 405

@app.route('/loscaballotesdeuniv/users/friends', methods=['POST'])
def addNewFriend():
        if request.method == 'POST':
            return UserHandler().addNewFriendByFriendID(request.json)
        else:
            return jsonify(Error="Method not allowed"), 405

@app.route('/loscaballotesdeuniv/users/<int:user_id>/friends/<int:friend_id>/delete', methods=['DELETE'])
def deleteFriendByFriendID(user_id, friend_id):
        if request.method == 'DELETE':
            return UserHandler().deleteFriendByFriendID(user_id, friend_id)
        else:
            return jsonify(Error="Method not allowed."), 405

@app.route("/loscaballotesdeuniv/users/<int:user_id>/<string:folder_name>", methods=['GET'])
def getEmailByFolderAndUserID(user_id, folder_name):
    # first letter of the folder_name should be uppercase
    if request.method == 'GET':
        return EmailHandler().getEmailByFolderAndUserID(user_id, folder_name)
    else:
        return jsonify(Error="Method not allowed"), 405




if __name__ == '__main__':
    app.run()
