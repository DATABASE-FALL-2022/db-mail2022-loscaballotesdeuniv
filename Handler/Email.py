from flask import jsonify
from DAO.Email import EmailDao


class EmailHandler:

    def build_email_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['ename'] = row[2]
        result['subject'] = row[3]
        result['body'] = row[4]
        result['emailtype'] = row[5]
        result['isread'] = row[6]
        result['wasdeleted'] = row[7]
        result['recipientid'] = row[8]
        return result


    def getAllUsersEmails(self):
        dao = EmailDao()
        emails_list = dao.getAllUsersEmails()
        return jsonify(emails_list)


    def getUserEmailsByIDENAME(self, user_id, ename):
        dao = EmailDao()
        emails_list = dao.getUserEmailsByIDENAME(user_id, ename)
        result_list = []
        for row in emails_list:
            result = self.build_email_dict(row)
            result_list.append(result)
        return jsonify(Emails=result_list)


    def deleteEmail(self, user_id, ename):
        dao = EmailDao()
        if not dao.getUserEmailsByIDENAME(user_id, ename):
            return jsonify(Error = "Email not found."), 404
        else:
            dao.delete(user_id, ename)
            return jsonify(DeleteStatus = "OK"), 200

    def getEmailByFolderAndUserID(self, user_id, folder_name):
        dao = EmailDao()
        emails_list = dao.getEmailByFolderAndUserID(user_id, folder_name)
        result_list = []
        for row in emails_list:
            result = self.build_email_dict(row)
            result_list.append(result)
        if result_list:
            return jsonify(Emails=result_list)
        else:
            return jsonify(Error="No emails in the folder")




