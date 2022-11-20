from flask import jsonify

import DAO.Email
from DAO.Email import EmailDao
from DAO.Folder import FolderDao
from DAO.User import UserDao

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
        result['recipientid'] = row[7]
        return result

    def build_email_attributes(self, user_id, eid, ename, subject, body, emailtype, isread, recipientid):
        result = {}
        result['user_id'] = user_id
        result['eid'] = eid
        result['ename'] = ename
        result['subject'] = subject
        result['body'] = body
        result['emailtype'] = emailtype
        result['isread'] = isread
        result['recipientid'] = recipientid
        return result

    def build_email_folder_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['ename'] = row[2]
        result['subject'] = row[3]
        result['body'] = row[4]
        result['emailtype'] = row[5]
        result['recipientid'] = row[6]
        result['folder_name'] = row[7]
        result['wasdeleted'] = row[8]
        return result

    def build_email_attributes(self, user_id, eid, ename, subject, body, emailtype, recipientid, folder_name, wasdeleted):
        result = {}
        result['user_id'] = user_id
        result['eid'] = eid
        result['ename'] = ename
        result['subject'] = subject
        result['body'] = body
        result['emailtype'] = emailtype
        result['recipientid'] = recipientid
        result['folder_name'] = folder_name
        result['wasdeleted'] = wasdeleted
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
    def getAllUsersEmailsByID(self, user_id):
        dao = EmailDao()
        emails_list = dao.getAllUsersEmailsByID(user_id,)
        result_list = []
        for row in emails_list:
            result = self.build_email_folder_dict(row)
            result_list.append(result)
        return jsonify(Emails=result_list)


    def deleteEmail(self, user_id, eid):
        dao = FolderDao()
        check = dao.deleteFromFolder(user_id, eid)
        if check:
            return jsonify("Email was deleted successfully")
        else:
            return jsonify("Error during deletion"), 404



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
            return jsonify(Error="No emails in the folder"), 404

    def createEmailJson(self, json):
        user_id = json['user_id']
        ename = json['ename']
        subject = json['subject']
        body = json['body']
        emailtype = json['emailtype']
        isread = json['isread']
        recipientid = json['recipientid']

        if user_id and ename and subject and body and emailtype and isread and recipientid:
            edao = EmailDao()
            fdao = FolderDao()
            eid = edao.insertNewEmail(user_id, ename, subject, body, emailtype, isread, recipientid)
            result = self.build_email_attributes(user_id, eid, ename, subject, body, emailtype, isread, recipientid)

            wasdeleted = False
            draft = "Draft"

            fcheck = fdao.insertIntoFolder(user_id, eid, draft, wasdeleted)

            if fcheck:
                return jsonify(Email=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def readEmail(self, user_id, eid):
        dao = EmailDao()

        email = dao.getEmailInInboxByUserID(user_id, eid)
        dao.readEmail(user_id, eid)

        result_list = []

        for row in email:
            result = self.build_email_dict(row)
            result_list.append(result)
        return result_list


