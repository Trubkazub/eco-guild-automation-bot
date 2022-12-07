from dotenv import dotenv_values
from connect_db import open_connection, close_connection

config = dotenv_values(".env")

def create_db(cursor):
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'eco_guild_mgu'")
    exists = cursor.fetchone()
    if not exists:
        sql_create_database = f"CREATE DATABASE eco_guild_mgu;"
        cursor.execute(sql_create_database)
        print('db eco_guild_mgu created')
    else:
        print('db eco_guild_mgu already exists')

USER = config['USER']
HOST = config['HOST']
PASSWORD = config['PASSWORD']
PORT = config['PORT']
DATABASE = config['DATABASE']

if __name__ == '__main__':
    connection = open_connection(USER, PASSWORD, HOST, PORT, 'postgres')
    cursor = connection.cursor()
    create_db(cursor)
    cursor.close()
    close_connection(connection)
