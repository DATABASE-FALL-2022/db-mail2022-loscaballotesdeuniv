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
