from Config.dbconfig import pg_config
import psycopg2

class UserDao:

    def __init__ (self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s " % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'],
                                                            pg_config['port'],
                                                            pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getUsersByID(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users where user_id = %s ;"
        cursor.execute(query, (user_id,))
        self.conn.commit()
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserEmailByID(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT firstname, lastname, user_id, email FROM users where user_id = %s ;"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    def insertNewUser(self, firstname, lastname, phone_number, date_of_birth, email, password, premiumuser, isfriend):
        cursor = self.conn.cursor()
        query = "INSERT INTO users(firstname, lastname, phone_number, date_of_birth, email, password, " \
                "premiumuser, isfriend) ""VALUES (%s, %s, %s, %s, %s, %s, %s, %s) returning user_id;"
        cursor.execute(query, (firstname, lastname, phone_number, date_of_birth, email, password, premiumuser, isfriend,))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def manageFriends(self, user_id, friend_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO isFriend(user_id, friend_id) values(%s,%s)"
        cursor.execute(query, (user_id, friend_id,))
        self.conn.commit()
        query = "INSERT INTO isFriend(user_id, friend_id) values(%s,%s)"
        cursor.execute(query, (friend_id, user_id,))
        self.conn.commit()
        cursor.close()
        return True

    def getAllUserFriends(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT email FROM isFriend NATURAL INNER JOIN Users where friend_id = %s;"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def deleteFriendByFriendID(self, user_id, friend_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM isFriend where user_id = %s AND friend_id = %s;"
        cursor.execute(query, (user_id, friend_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        cursor = self.conn.cursor()
        query = "DELETE FROM isFriend where user_id = %s AND friend_id = %s;"
        cursor.execute(query, (friend_id, user_id,))
        affected_rows2 = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        cursor.close()
        return affected_rows != 0 and affected_rows2 != 0

    def isPremiumuser(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT premiumuser FROM users where user_id = %s"
        cursor.execute(query, (user_id,))
        premium = cursor.fetchone()[0]
        self.conn.commit()
        return premium
