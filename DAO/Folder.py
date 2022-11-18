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
