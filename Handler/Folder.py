from flask import jsonify
from DAO.Folder import FolderDao
from DAO.User import UserDao


class FolderHandler:

    def build_folder_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['fdname'] = row[2]
        result['wasdeleted'] = row[3]
        result['wasread'] = row[4]
        result['fromfriend'] = row[5]
        return result

    def build_folder_attributes(self, user_id, eid, folder_name, wasdeleted, wasread, fromfriend):
        result = {}
        result['user_id'] = user_id
        result['eid'] = eid
        result['folder_name'] = folder_name
        result['wasdeleted'] = wasdeleted
        result['wasread'] = wasread
        result['fromfriend'] = fromfriend
        return result

    def getAllFolders(self):
        dao = FolderDao()
        folder_list = dao.getAllFolders()
        result_list = []
        for row in folder_list:
            result = self.build_folder_dict(row)
            result_list.append(result)
        return jsonify(Folders=result_list)
    def getUsersFolderByID(self, user_id):
        dao = FolderDao()
        user_list = dao.getUsersFolderByID(user_id)
        return jsonify(Users_Folders=user_list)

    def insertFolderJson(self, json):
        user_id = json['user_id']
        eid = json['eid']
        folder_name = json['folder_name']
        wasdeleted = json['wasdeleted']
        wasread = False
        fromfriend = json['fromfriend']

        if user_id and eid and folder_name and wasdeleted and fromfriend:
            dao = FolderDao()
            result = self.build_folder_attributes(user_id, eid, folder_name, wasdeleted, wasread, fromfriend)
            check = dao.insertIntoFolder(user_id, eid, folder_name, wasdeleted, wasread, fromfriend)
            if check:
                return jsonify(Folder=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteFromFolder(self, user_id, eid):
        dao = FolderDao()
        result = dao.deleteFromFolder(user_id, eid)
        if result == True:
            return jsonify("Item deleted from folder")
        else:
            return jsonify("Error, could not delete"), 404

    def getUserIDByEID(self, eid):
        dao = FolderDao()
        folder_list = dao.getUserIDByEID(eid)
        return jsonify(Folders=folder_list)

    def sendEmail(self, user_id, recipient_id, eid):
        fdao = FolderDao()
        udao = UserDao()
        result = fdao.sendEmail(user_id, recipient_id, eid)
        if result:
            friendcheck = udao.isFriend(user_id, recipient_id)
            if friendcheck:
                friend = True
                fdao.updateFromFriend(user_id, eid, friend)
                fdao.updateFromFriend(recipient_id, eid, friend)
            return jsonify("Email was sent successfully")
        else:
            return jsonify(Error="Email could not be sent"), 404
