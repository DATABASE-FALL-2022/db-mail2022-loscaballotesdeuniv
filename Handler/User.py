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
        return result

    def build_user_attributes(self, user_id, firstname, lastname, phone_number, date_of_birth, email, password,
                              premiumuser):
        result = {}
        result['user_id'] = user_id
        result['firstname'] = firstname
        result['lastname'] = lastname
        result['phone_number'] = phone_number
        result['date_of_birth'] = date_of_birth
        result['email'] = email
        result['password'] = password
        result['premiumuser'] = premiumuser
        return result

    def getAllUsers(self):
        dao = UserDao()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            result = self.build_user_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def getUsersByID(self, user_id):
        dao = UserDao()
        user_list = dao.getUsersByID(user_id)
        return jsonify(User=user_list)

    def getUserEmailByID(self, user_id):
        dao = UserDao()
        emails_list = dao.getUserEmailByID(user_id)
        return jsonify(Users_Email=emails_list)

    def addNewUserJson(self, json):
        firstname = json['firstname']
        lastname = json['lastname']
        phone_number = json['phone_number']
        date_of_birth = json['date_of_birth']
        email = json['email']
        password = json['password']
        premiumuser = 'false'
        if firstname and lastname and phone_number and date_of_birth and email and password:
            dao = UserDao()
            user_id = dao.insertNewUser(firstname, lastname, phone_number, date_of_birth, email, password, premiumuser)
            result = self.build_user_attributes(user_id, firstname, lastname, phone_number, date_of_birth, email, password, premiumuser)
            return jsonify(User=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400


    def build_isfriend_dict(self, row):
            result = {}
            result['user_id'] = row[0]
            result['friend_id'] = row[1]
            return result

    def getAllUserFriends(self, friend_id):
        dao = UserDao()
        friends_list = dao.getAllUserFriends(friend_id)
        return jsonify(Friends=friends_list)

    def addNewFriendByFriendID(self, json):
        user_id = json['user_id']
        friend_id = json['friend_id']
        dao = UserDao()
        dao.manageFriends(user_id, friend_id)
        return jsonify("FRIEND RELATIONSHIP MADE SUCCESSFULLY"), 201

    def deleteFriendByFriendID(self, user_id, friend_id):
        dao = UserDao()
        result = dao.deleteFriendByFriendID(user_id, friend_id)
        if result:
            return jsonify("FRIEND RELATIONSHIP HAS BEEN DELETED SUCCESSFULLY"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def isPremiumuser(self, user_id):
        dao = UserDao()
        result = dao.isPremiumuser(user_id)
        if result == True:
            return jsonify("Person is a Premium User")
        else:
            return jsonify("Person is Not a Premium User"), 404
