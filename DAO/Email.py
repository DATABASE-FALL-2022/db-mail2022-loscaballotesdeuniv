from Config.dbconfig import pg_config
import psycopg2


class EmailDao:


    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s " % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'],
                                                            pg_config['port'],
                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)


    def getAllUsersEmails(self):
        cursor = self.conn.cursor()
        query = "SELECT email FROM users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result


    def getUserEmailsByIDENAME(self, user_id, ename):
        cursor = self.conn.cursor()
        query = "SELECT * FROM email where user_id = %s and ename = %s;"
        cursor.execute(query, (user_id, ename,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUsersEmailsByID(self, user_id):
        cursor = self.conn.cursor()
        query = "select email.user_id, email.eid, ename, subject, body, emailtype, recipientid, folder_name, wasdeleted, wasread " \
                "from email join folders as f on email.eid = f.eid " \
                "where f.user_id = %s " \
                "and folder_name <> 'Draft' " \
                "and wasdeleted = 'false';"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def deleteEmail(self, user_id, ename): #tobechanged
        #edao = EmailDao()
        # cursor = self.conn.cursor()
        # query = "delete from email where user_id = %s and ename = %s;"
        # cursor.execute(query, (user_id, ename,))
        # self.conn.commit()
        # return ename'
        return

    def insertNewEmail(self, user_id, ename, subject, body, emailtype, isread, recipientid):
        cursor = self.conn.cursor()
        query = "INSERT INTO email(user_id, ename, subject, body, emailtype, isread, " \
                "recipientid) VALUES (%s, %s, %s, %s, %s, %s, %s) returning eid;"
        cursor.execute(query, (user_id, ename, subject, body, emailtype, isread, recipientid,))
        eid = cursor.fetchone()[0]
        self.conn.commit()
        return eid

    def getEmailByFolderAndUserID(self, user_id, folder_name):
        cursor = self.conn.cursor()
        query = "select email.user_id, email.eid, ename, subject, body, emailtype, isread, recipientid " \
                "from email join folders f on email.eid = f.eid where f.user_id = %s and folder_name = %s and wasdeleted = false " \
                "ORDER BY eid DESC"
        cursor.execute(query, (user_id, folder_name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getEmailInInboxByUserID(self, user_id, eid):
        cursor = self.conn.cursor()
        query = "select e.user_id, e.eid, ename, subject, body, emailtype, isread, recipientid " \
                "from email as e join folders as f on e.eid = f.eid where f.user_id = %s and f.eid = %s and " \
                "folder_name = 'Inbox' limit 1"
        cursor.execute(query, (user_id, eid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def readEmail(self, user_id, eid):
        cursor = self.conn.cursor()

        queryToSendMessageRead = "insert into email (user_id, ename, subject, body, emailtype, isread, recipientid) " \
                                 "values (34, 'Automated Message', 'Read Notification', " \
                                 "'The email sent was read by the recipient.', 'To', false, (select user_id from " \
                                 "email where recipientid = %s and eid = %s limit 1));"
        cursor.execute(queryToSendMessageRead, (user_id, eid))
        self.conn.commit()

        queryToUpdateInbox = "insert into folders (user_id, eid, folder_name, wasdeleted, wasread) " \
                             "values ((select user_id from email where eid = %s and recipientid = %s limit 1), " \
                             "(select eid from email where user_id = 34 and recipientid = (select user_id from " \
                             "email where eid = %s and recipientid = %s limit 1) limit 1), " \
                             "'Inbox', false, false) returning true;"
        cursor.execute(queryToUpdateInbox, (eid, user_id, eid, user_id))
        self.conn.commit()

        queryToUpdateOutbox = "insert into folders (user_id, eid, folder_name, wasdeleted, wasread) " \
                              "values (34, (select eid from email where user_id = 34 and recipientid" \
                              " = (select user_id from " \
                              "email where eid = %s and recipientid = %s limit 1) limit 1), " \
                              "'Outbox', false, false);"
        cursor.execute(queryToUpdateOutbox, (eid, user_id,))
        self.conn.commit()

        queryToUpdateIsRead = "update folders set wasread = True where user_id = %s and eid = %s and folder_name = 'Inbox'"
        cursor.execute(queryToUpdateIsRead, (user_id, eid,))
        self.conn.commit()

        if queryToUpdateInbox and queryToSendMessageRead and queryToUpdateOutbox:
            return True
        else:
            return False


