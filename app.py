from flask import Flask, jsonify, request, send_file
from Handler.User import UserHandler

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def greeting():
    return "Los Caballotes de la Universidad"

@app.route('/register')
def registerUser():
    return send_file("register.html")

@app.route('/register/verification', methods=["POST"])
def verifyRegistration():
    first_name = request.form['user_fname']
    last_name = request.form['user_lname']
    password = request.form['user_password']
    date_of_birth = request.form['user_dob']
    email = request.form['new_email']
    phone_number = request.form['user_pnumber']

    #Este return es para que vean que los parametros pasaron del form de la pagina aqui
    #Lo siguiente seria crear una forma de verificar el email con los emails de la base de datos
    #Este codigo no es perfecto pero lo hice como en una hora xD
    return first_name + last_name + password + date_of_birth + email + phone_number

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
