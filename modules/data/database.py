import mysql.connector

from .config import Config


class MysqlConnection:
    def __init__(self, config: Config):
        self.config = config
        self.host = config.db_host
        self.user = config.db_user
        self.password = config.db_password
        self.db = config.db_database

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db
            )
        except mysql.connector.DatabaseError as e:
            raise e

        return connection

    def select(self, *query) -> tuple:
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute(*query)
                return cursor.fetchall()
        finally:
            if 'connection' in locals():
                connection.close()

    def insert_or_update(self, query) -> bool:
        connection = self.connect()

        try:
            with connection.cursor() as cursor:

                cursor.execute(query)

                if not cursor.rowcount:
                    return False
                else:
                    connection.commit()
                    return True
        finally:
            connection.close()
