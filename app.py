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

@app.route('/loscaballotesdeuniv/emails', methods=['GET'])
def getAllUserEmails():
    return EmailHandler().getAllUsersEmails()

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




if __name__ == '__main__':
    app.run()
