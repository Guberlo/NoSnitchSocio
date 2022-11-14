import mysql.connector

from mysql.connector.constants import ClientFlag

from .config import Config


class MysqlConnection:
    def __init__(self, config: Config):
        self.config = config
        self.host = config.db_host
        self.user = config.db_user
        self.password = config.db_password
        self.db = config.db_database
        self.ca_location = config.db_ca_location
        self.port = config.db_port

    def connect(self):
        mysql_config = {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'client_flags': [ClientFlag.SSL],
            'ssl_ca': self.ca_location,
            'port': self.port,
            'database': self.db
        }

        try:
            connection = mysql.connector.connect(**mysql_config)
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
