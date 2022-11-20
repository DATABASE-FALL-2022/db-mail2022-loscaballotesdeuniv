from flask import jsonify
from DAO.Folder import FolderDao


class FolderHandler:

    def build_folder_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['fdname'] = row[2]
        result['wasdeleted'] = row[3]
        return result


    def build_folder_attributes(self, user_id, eid, folder_name, wasdeleted):
        result = {}
        result['user_id'] = user_id
        result['eid'] = eid
        result['folder_name'] = folder_name
        result['wasdeleted'] = wasdeleted
        return result

    def getAllFolders(self):
        dao = FolderDao()
        folder_list = dao.getAllFolders()
        result_list = []
        for row in folder_list:
            result = self.build_folder_dict(row)
            result_list.append(result)
        return jsonify(Folders=result_list)




    def insertFolderJson(self, json):
        user_id = json['user_id']
        eid = json['eid']
        folder_name = json['folder_name']
        wasdeleted = json['wasdeleted']

        if user_id and eid and folder_name and wasdeleted:
            dao = FolderDao()
            result = self.build_folder_attributes(user_id, eid, folder_name, wasdeleted)
            check = dao.insertIntoFolder(user_id, eid, folder_name, wasdeleted)
            if check:
                return jsonify(Folder=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400
