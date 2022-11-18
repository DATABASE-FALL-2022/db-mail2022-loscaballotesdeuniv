from flask import jsonify
from DAO.Folder import FolderDao


class FolderHandler:

    def build_folder_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['fdname'] = row[2]
        return result

    def getAllFolders(self):
        dao = FolderDao()
        folder_list = dao.getAllFolders()
        result_list = []
        for row in folder_list:
            result = self.build_folder_dict(row)
            result_list.append(result)
        return jsonify(Folders=result_list)
