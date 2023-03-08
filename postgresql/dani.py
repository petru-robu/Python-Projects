import random
from datetime import *
from utils import Utils

import psycopg2


class DataBase:

    def _init_(self):
        self.db_name = 'ing_software'
        self.db_user = 'postgres'
        self.db_password = 'root'
        self.host = '127.0.0.1'
        self.port = '54321'
        self.utils = Utils()

    def get_number_of_records(self, username: str):

        try:
            # Establishing the connection
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            # Select from database
            cursor.execute(f"SELECT * FROM APP_USERS WHERE UPPER(USERNAME) = '{username.upper()}'")

            app_records = cursor.fetchall()

            if len(app_records) <= 2:
                return len(app_records)

        except Exception as e:
            print("Error when getting the info about a user : ", e)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_timestamp_of_last_record(self, username: str):

        try:
            # Establishing the connection
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            # Select from database
            cursor.execute(f"SELECT * FROM APP_USERS WHERE UPPER(USERNAME) = '{username.upper()}' ORDER BY ORDER_NUMBER")

            app_records = cursor.fetchall()

            if len(app_records) == 0:
                raise AssertionError

            return app_records[0][3]

        except Exception as e:
            print("Error when getting the info about a user : ", e)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_records(self, username: str):
        try:
            # Establishing the connection
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            # Select from database
            cursor.execute(
                f"SELECT * FROM APP_USERS WHERE UPPER(USERNAME) = '{username.upper()}' ORDER BY ORDER_NUMBER")

            app_records = cursor.fetchall()

            return app_records

        except Exception as e:
            print("Error when getting the info about a user : ", e)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self, username: str, followers: list, following: list, number: int):

        try:
            # Establishing the connection
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            # Insert into database
            cursor.execute(
                f'''
                INSERT INTO APP_USERS 
                VALUES(
                    '{username.lower()}',
                    '{self.utils.serialize(followers)}',
                    '{self.utils.serialize(following)}', 
                    default, 
                    {number}
                );'''
            )

            # Commit the changes
            conn.commit()
        except Exception as e:
            print("Error when getting the info about a user : ", e)
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update(self, username: str, followers: list, following: list, number: int):
        try:
            # Establishing the connection
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            # Insert into database
            sql = f"""
                    UPDATE APP_USERS 
                    SET FOLLOWING = '{self.utils.serialize(following)}', 
                        FOLLOWERS = '{self.utils.serialize(followers)}' , 
                        TIMESTAMP  = DEFAULT,
                        ORDER_NUMBER = {number}
                    WHERE USERNAME = '{username.lower()}';
                    """

            cursor.execute(sql)

            # Commit the changes
            conn.commit()
        except Exception as e:
            print("Error when getting the info about a user : ", e)
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_with_permutation(self, username: str, followers: list, following: list, delete_from_db=True):
        try:
            # Establishing the connection
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            if delete_from_db:
                cursor.execute(
                    f"DELETE FROM APP_USERS WHERE UPPER(USERNAME) = '{username.upper()}' AND ORDER_NUMBER = 2")

            # Insert into database
            sql = f"""
                    UPDATE APP_USERS 
                    SET ORDER_NUMBER = 2
                    WHERE USERNAME = '{username.lower()}' AND ORDER_NUMBER = 1;
                    """

            cursor.execute(sql)

            cursor.execute(
                f'''
                            INSERT INTO APP_USERS
                            VALUES(
                                '{username.lower()}',
                                '{self.utils.serialize(followers)}',
                                '{self.utils.serialize(following)}',
                                default,
                                1
                            );'''
            )

            # Commit the changes
            conn.commit()
        except Exception as e:
            print("Error when getting the info about a user : ", e)
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_with_post(self, username: str, followers: list, following: list):
        self.update_with_permutation(username, followers, following, False)

    def create_table(self):

        # Establishing the connection
        conn = psycopg2.connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.host,
            port=self.port
        )
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Doping EMPLOYEE table if already exists.
        cursor.execute("DROP TABLE IF EXISTS APP_USERS")

        # Creating table as per requirement
        sql = '''CREATE TABLE APP_USERS(
           USERNAME TEXT NOT NULL,
           FOLLOWERS TEXT,
           FOLLOWING TEXT,
           TIMESTAMP timestamptz NOT NULL DEFAULT now(),
           ORDER_NUMBER integer NOT NULL
        )'''

        cursor.execute(sql)

        print("Table created successfully........")
        conn.commit()
        # Closing the connection
        conn.close()


# db.update('dani', ['alu', 'pigus'], ['benten'])
# print(db.get_info_from_username('dani'))
#
# # db.post_info('test001', 'dani,melisa,roxana', 'roxana,melisa')
#
# print(db.get_info_from_username('roxi'))

# db = DataBase()
# db.update_with_permutation('test001', ['aaaa','b','c'], ['aaaa','b','e'])