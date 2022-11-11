from flask import Flask, jsonify, request
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
        print("REQUEST: ", request.json)
        return UserHandler().insertUserJson(request.json)
    else:
        if not request.args:
            return UserHandler().getAllUsers()



if __name__ == '__main__':
    app.run()
