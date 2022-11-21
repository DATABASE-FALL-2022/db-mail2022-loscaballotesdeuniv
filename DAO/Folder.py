from Config.dbconfig import pg_config
import psycopg2

class FolderDao:


    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s " % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'],
                                                            pg_config['port'],
                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllFolders(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM folders"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersFolderByID(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT user_id, email, folder_name, eid, wasdeleted, wasread FROM users natural inner join folders where user_id = %s;"
        cursor.execute(query, (user_id,))
        self.conn.commit()
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertIntoFolder(self, user_id, eid, folder_name, wasdeleted, wasread, fromfriend):
        cursor = self.conn.cursor()
        query = "INSERT INTO folders(user_id, eid, folder_name, wasdeleted, wasread, fromfriend) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(query, (user_id, eid, folder_name, wasdeleted, wasread, fromfriend,))
        self.conn.commit()
        return True

    def deleteFromFolder(self, user_id, eid): # used for delete email
        deleted = True;
        cursor = self.conn.cursor()
        query = "update folders set wasdeleted = %s where user_id = %s and eid = %s;"
        cursor.execute(query, (deleted, user_id, eid,))
        self.conn.commit()
        query2 = "update folders set wasdeleted = %s where eid = %s and folder_name = 'Inbox' and " \
                 "(select premiumuser from users where user_id = %s limit 1) = true;"
        cursor.execute(query2, (deleted, eid, user_id,))
        self.conn.commit()
        return True

    def sendEmail(self, user_id, recipient_id, eid):
        cursor = self.conn.cursor()
        query1 = "update folders  set folder_name = 'Outbox' where  user_id = (select user_id " \
                 "from email where email.user_id = %s and email.eid = %s and folder_name = 'Draft' limit 1) and eid = " \
                 "(select email.eid from email where email.user_id = %s and email.eid = %s limit 1) " \
                 "and wasdeleted = 'False' and fromfriend = 'False' returning True"
        cursor.execute(query1, (user_id, eid, user_id, eid))
        self.conn.commit()
        if cursor:
            query2 = "insert into folders values ((select recipientid from email where email.user_id = %s" \
                     " and email.eid = %s and recipientid = %s limit 1), (select email.eid from email " \
                     "where email.user_id = %s and email.eid = %s and recipientid = %s limit 1), 'Inbox', False, False) " \
                     "returning True;"
            cursor.execute(query2, (user_id, eid, recipient_id, user_id, eid, recipient_id))
            self.conn.commit()
            return True
        else:
            return False
    def changeFolderOutbox(self, user_id, eid, folder_name):
        cursor = self.conn.cursor()
        previousfolder = self.getFolder(user_id, eid)
        query = "update folders set folder_name = %s where user_id = %s and eid = %s and folder_name = 'Outbox' and " \
                 "(select premiumuser from users where user_id = %s limit 1) = true;"
        cursor.execute(query, (folder_name, user_id, eid, user_id,))
        self.conn.commit()
        return previousfolder


    def getFolder(self, user_id, eid):
        cursor = self.conn.cursor()
        query = "select folder_name from folders where user_id=%s and eid = %s;"
        cursor.execute(query, (user_id, eid,))
        folder = cursor.fetchone()[0]
        self.conn.commit()
        return folder

    def sendReplyEmail(self, user_sent, user_to, reply_eid):
        cursor = self.conn.cursor()
        query1 = "update folders  set folder_name = 'Outbox' where  user_id = (select user_id " \
                 "from email where email.user_id = %s and email.eid = %s and folder_name = 'DraftToReply' " \
                 "limit 1) and eid = " \
                 "(select email.eid from email where email.user_id = %s and email.eid = %s limit 1) " \
                 "and wasdeleted = 'False'  returning True"
        cursor.execute(query1, (user_sent, reply_eid, user_sent, reply_eid))
        self.conn.commit()
        if cursor:
            query2 = "insert into folders values (%s, %s, 'Replies', False, False, False) " \
                     "returning True;"
            cursor.execute(query2, (user_to, reply_eid,))
            self.conn.commit()
            return True
        else:
            return False


    def updateFromFriend(self, user_id, eid, fromfriend):
        cursor = self.conn.cursor()
        query = "update folders set fromfriend = %s where user_id = %s and eid = %s;"
        cursor.execute(query, (fromfriend, user_id, eid,))
        self.conn.commit()
        return True


    def changeFolder(self, user_id, eid, folder_name):
        cursor = self.conn.cursor()
        query = "update folders set folder_name = %s where user_id = %s and eid = %s"
        cursor.execute(query, (folder_name, user_id, eid,))
        self.conn.commit()
        return True

