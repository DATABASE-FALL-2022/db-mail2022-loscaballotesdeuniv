from Config.dbconfig import pg_config
import psycopg2

class UserDao:
    def __init__ (self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s " % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'],
                                                            pg_config['port'],
                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users;"
        cursor.execute(query)
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

    def delete(self, user_id, ename):
        cursor = self.conn.cursor()
        query = "delete from email where user_id = %s and ename = %s;"
        cursor.execute(query, (user_id, ename,))
        self.conn.commit()
        return ename

