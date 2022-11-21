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
        query = "select email.user_id, email.eid, ename, subject, body, emailtype, recipientid, folder_name, wasdeleted, wasread, fromfriend " \
                "from email join folders as f on email.eid = f.eid " \
                "where f.user_id = %s " \
                "and folder_name <> 'Draft' " \
                "and wasdeleted = 'false';"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertNewEmail(self, user_id, ename, subject, body, emailtype, recipientid):
        cursor = self.conn.cursor()
        query = "INSERT INTO email(user_id, ename, subject, body, emailtype,  " \
                "recipientid) VALUES (%s, %s, %s, %s, %s, %s) returning eid;"
        cursor.execute(query, (user_id, ename, subject, body, emailtype, recipientid,))
        eid = cursor.fetchone()[0]
        self.conn.commit()
        return eid

    def getEmailByFolderAndUserID(self, user_id, folder_name):
        cursor = self.conn.cursor()
        query = "select email.user_id, email.eid, ename, subject, body, emailtype, recipientid " \
                "from email join folders f on email.eid = f.eid where f.user_id = %s and folder_name = %s and wasdeleted = false " \
                "ORDER BY eid DESC"
        cursor.execute(query, (user_id, folder_name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getEmailInInboxByUserID(self, user_id, eid):
        cursor = self.conn.cursor()
        query = "select e.user_id, e.eid, ename, subject, body, emailtype, recipientid " \
                "from email as e join folders as f on e.eid = f.eid where f.user_id = %s and f.eid = %s and " \
                "(folder_name = 'Inbox' or folder_name = 'Replies') limit 1"
        cursor.execute(query, (user_id, eid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def readEmail(self, user_id, eid):
        cursor = self.conn.cursor()

        queryToSendMessageRead = "insert into email (user_id, ename, subject, body, emailtype, recipientid) " \
                                 "values (34, 'Automated Message', 'Read Notification', " \
                                 "'The email sent was read by the recipient.', 'To', (select user_id from " \
                                 "email where recipientid = %s and eid = %s limit 1));"
        cursor.execute(queryToSendMessageRead, (user_id, eid))
        self.conn.commit()

        queryToUpdateInbox = "insert into folders (user_id, eid, folder_name, wasdeleted, wasread, fromfriend) " \
                             "values ((select user_id from email where eid = %s and recipientid = %s limit 1), " \
                             "(select eid from email where user_id = 34 and recipientid = (select user_id from " \
                             "email where eid = %s and recipientid = %s limit 1) limit 1), " \
                             "'Inbox', false, false, false) returning true;"
        cursor.execute(queryToUpdateInbox, (eid, user_id, eid, user_id))
        self.conn.commit()

        queryToUpdateOutbox = "insert into folders (user_id, eid, folder_name, wasdeleted, wasread, fromfriend) " \
                              "values (34, (select eid from email where user_id = 34 and recipientid" \
                              " = (select user_id from " \
                              "email where eid = %s and recipientid = %s limit 1) limit 1), " \
                              "'Outbox', false, false, false);"
        cursor.execute(queryToUpdateOutbox, (eid, user_id,))
        self.conn.commit()

        queryToUpdateIsRead = "update folders set wasread = True where user_id = %s and eid = %s and folder_name = 'Inbox'"
        cursor.execute(queryToUpdateIsRead, (user_id, eid,))
        self.conn.commit()

        if queryToUpdateInbox and queryToSendMessageRead and queryToUpdateOutbox:
            return True
        else:
            return False

    def editEmail(self, user_id, eid, ename, subject, body, emailtype, recipientid):
        cursor = self.conn.cursor()
        if ename:
            query = "update email set ename = %s where user_id = %s and eid = %s;"
            cursor.execute(query, (ename, user_id, eid))
            self.conn.commit()
        if subject:
            query = "update email set subject = %s where user_id = %s and eid = %s;"
            cursor.execute(query, (subject, user_id, eid))
            self.conn.commit()
        if body:
            query = "update email set body = %s where user_id = %s and eid = %s;"
            cursor.execute(query, (body, user_id, eid))
            self.conn.commit()
        if emailtype:
            query = "update email set emailtype = %s where user_id = %s and eid = %s;"
            cursor.execute(query, (emailtype, user_id, eid))
            self.conn.commit()
        if recipientid:
            query = "update email set recipientid = %s where user_id = %s and eid = %s;"
            cursor.execute(query, (recipientid, user_id, eid))
            self.conn.commit()

        return True

    def getEmailwithMostRecipients(self):
        cursor = self.conn.cursor()
        query = "select *, ((select count(eid) as reccount " \
                "from folders " \
                "where folder_name = 'Inbox' or folder_name = 'Inbox/Favorite' " \
                "group by eid " \
                "order by reccount desc " \
                "limit 1))" \
                "from email " \
                "where eid = (with maxrecipients as (select count(eid) as reccount " \
                "from folders " \
                "where folder_name = 'Inbox' or folder_name = 'Inbox/Favorite' " \
                "group by eid " \
                "order by reccount desc) " \
                "select folders.eid " \
                "from folders natural inner join maxrecipients " \
                "limit 1) " \
                "limit 1"
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getEmailwithMostReplies(self):
        cursor = self.conn.cursor()
        query = "with maxreplies as (select count(folder_name) as countf " \
                "from folders " \
                "where folder_name = 'Replies' or folder_name = 'Replies/Favorite' " \
                "group by  eid " \
                "order by countf desc " \
                "limit 1)" \
                "select * " \
                "from folders natural inner join maxreplies " \
                "where folder_name = 'Replies' or folder_name = 'Replies/Favorite' " \
                "limit 1;"
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTop10UsersWithMoreEmailsInbox(self):
        cursor = self.conn.cursor()
        query = "select user_id, firstname, lastname, email, count(folder_name) as countf " \
                "from folders natural inner join users " \
                "where folder_name = 'Inbox' or folder_name = 'Inbox/Favorite' " \
                "group by  user_id, firstname, lastname, email " \
                "order by countf desc " \
                "limit 10;"
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTop10UsersWithMoreEmailsOutbox(self):
        cursor = self.conn.cursor()
        query = "select user_id, firstname, lastname, email, count(folder_name) as countf " \
                "from folders natural inner join users " \
                "where folder_name = 'Outbox' or folder_name = 'Outbox/Favorite' " \
                "group by  user_id, firstname, lastname, email " \
                "order by countf desc " \
                "limit 10;"
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getUsersEmailMostRecipients(self, user_id):
        cursor = self.conn.cursor()
        query = "with maxrecipients as ( select count(recipientid) as reccount " \
                "from email where user_id = %s " \
                "group by recipientid limit 1) " \
                "select * " \
                "from email natural inner join maxrecipients " \
                "where user_id = %s " \
                "limit 1"
        cursor.execute(query, (user_id, user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersEmailMostReplies(self, user_id):
        cursor = self.conn.cursor()
        query = "with maxreplies as (select count(folder_name) as countf " \
                "from folders " \
                "where (folder_name = 'Replies' or folder_name = 'Replies/Favorite') and user_id = %s " \
                "group by  eid " \
                "order by countf desc " \
                "limit 1) " \
                "select * " \
                "from email natural inner join maxreplies " \
                "where user_id = %s " \
                "limit 1;"
        cursor.execute(query, (user_id,user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTop5UsersYouSend(self, user_id):
        cursor = self.conn.cursor()
        query = "select recipientid, count(folder_name) as countf " \
                "from folders natural inner join users natural inner join email " \
                "where user_id = %s " \
                "and (folder_name = 'Outbox'or folder_name = 'Outbox/Favorite') and user_id = %s " \
                "group by recipientid " \
                "order by countf desc " \
                "limit 5;"
        cursor.execute(query, (user_id,user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTop5UsersYouRecieve(self, user_id):
        cursor = self.conn.cursor()
        query = "select user_id, email, count(recipientid) as userrecieves " \
                "from users natural inner join email " \
                "where recipientid = %s " \
                "group by user_id, users.email " \
                "order by userrecieves desc " \
                "limit 5;"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
