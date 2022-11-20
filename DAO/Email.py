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

