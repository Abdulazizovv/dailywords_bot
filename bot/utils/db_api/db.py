import psycopg2
from bot.data import config

class DataBase(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname='lesson_2',
            user='postgres',
            password="boburiy",
            host='localhost',
            port=1612
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tg_user(
                            id SERIAL PRIMARY KEY,
                            tg_id BIGINT UNIQUE NOT NULL,
                            first_name VARCHAR(255) NOT NULL,
                            last_name VARCHAR(255) NULL,
                            username VARCHAR(255) NULL,
                            reg_date TIMESTAMP DEFAULT NOW()
                            )
                            ''')
    def add_user(self, tg_id, username, first_name, last_name):
        print("add_user")
        print(username, first_name, last_name, tg_id)

        

        self.cursor.execute('''INSERT INTO tg_user(tg_id, username, first_name, last_name) 
                            VALUES (%s, %s, %s, %s) ON CONFLICT (tg_id) DO NOTHING''',
                            (tg_id, username, first_name, last_name))
        self.connection.commit()
    def user_exists(self,tg_id):
        self.cursor.execute(f'''SELECT tg_id FROM tg_user WHERE tg_id={tg_id}''')
        return bool(self.cursor.fetchall())

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS category(
                            id SERIAL PRIMARY KEY,
                            category_name VARCHAR(255) NOT NULL,
                            reg_date TIMESTAMP DEFAULT NOW()
                            )
                            ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS book(
                            id SERIAL PRIMARY KEY,
                            category_id INT REFERENCES category(id) ON DELETE CASCADE,
                            book_name VARCHAR(255) NOT NULL,
                            book_file VARCHAR(255) NOT NULL,
                            reg_date TIMESTAMP DEFAULT NOW()
                            )
                            ''')
        self.connection.commit()