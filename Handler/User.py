from flask import jsonify
from DAO.User import UserDao

class UserHandler:

    def build_user_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        result['phone_number'] = row[3]
        result['date_of_birth'] = row[4]
        result['email'] = row[5]
        result['password'] = row[6]
        result['premiumuser'] = row[7]
        result['isfriend'] = row[8]
        return result

    def build_user_attributes(self, user_id, firstname, lastname, phone_number, date_of_birth, email, password,
                              premiumuser, isfriend):
        result = {}
        result['user_id'] = user_id
        result['firstname'] = firstname
        result['lastname'] = lastname
        result['phone_number'] = phone_number
        result['date_of_birth'] = date_of_birth
        result['email'] = email
        result['password'] = password
        result['premiumuser'] = premiumuser
        result['isfriend'] = isfriend
        return result

    def getAllUsers(self):
        dao = UserDao()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            result = self.build_user_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def addNewUser(self, form):
        print("form: ", form)
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
            firstname = form['firstname']
            lastname = form['lastname']
            phone_number = form['phone_number']
            date_of_birth = form['date_of_birth']
            email = form['email']
            password = form['password']
            premiumuser = form['premiumuser']
            isfriend = form['isfriend']
            if firstname and lastname and phonenumber and date_of_birth and \
                    email and password and premiumuser and isfriend:
                dao = UserDao()
                user_id = dao.insertNewUser(firstname, lastname, phonenumber,
                                            date_of_birth, email, password, premiumuser,isfriend)

                result = self.build_user_attributes(user_id, firstname, lastname, phonenumber, date_of_birth,
                                                    email, password, premiumuser, isfriend)
                json["user_id"] = user_id
                return jsonify(json), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def addNewUserJson(self, json):
        firstname = json['firstname']
        lastname = json['lastname']
        phone_number = json['phone_number']
        date_of_birth = json['date_of_birth']
        email = json['email']
        password = json['password']
        premiumuser = json['premiumuser']
        isfriend = json['isfriend']

        if firstname and lastname and phone_number and date_of_birth and email and password and premiumuser and isfriend:
            dao = UserDao()
            user_id = dao.insertNewUser(firstname, lastname, phone_number, date_of_birth, email, password, premiumuser, isfriend)
            result = self.build_user_attributes(user_id, firstname, lastname, phone_number, date_of_birth, email, password, premiumuser, isfriend)
            return jsonify(User=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400


