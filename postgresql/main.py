import psycopg2

class Database:
    def __init__(self):
        self.db_name = 'prega_info'
        self.db_user = 'postgres'
        self.db_password = 'admin'
        self.host = '127.0.0.1'
        self.port = '54321'

        self.conn = psycopg2.connect(
            database = self.db_name,
            user = self.db_user,
            password = self.db_password,
            host = self.host,
            port = self.port
        )

    def __del__(self):
        print(123)
        self.conn.close()

    def createTable(self):
        cursor = self.conn.cursor()
        query = '''
            CREATE TABLE IF NOT EXISTS TEST1
            (
                ID INTEGER PRIMARY KEY,
                NUME TEXT NOT NULL,
                CNP INTEGER
            ) 
        '''
        cursor.execute(query)
        self.conn.commit()


db = Database()
db.createTable()