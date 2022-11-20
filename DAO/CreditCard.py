from Config.dbconfig import pg_config
import psycopg2


class CreditCardDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s " % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'],
                                                            pg_config['port'],
                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)


    def getAllUsersCreditCards(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM creditcard"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersCreditCardByID(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM creditcard  where user_id = %s;"
        cursor.execute(query, (user_id,))
        self.conn.commit()
        result = []
        for row in cursor:
            result.append(row)
        return result
