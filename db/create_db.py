from dotenv import dotenv_values
from connect_db import open_connection, close_connection

config = dotenv_values(".env")

def create_db(db_name, cursor):
    sql_create_database = f'CREATE DATABASE {db_name};'
    cursor.execute(sql_create_database)
    print(f'db {db_name} created')

USER = config['USER']
HOST = config['HOST']
PASSWORD = config['PASSWORD']
PORT = config['PORT']
DATABASE = config['DATABASE']

if __name__ == '__main__':
    connection = open_connection(USER, PASSWORD, HOST, PORT, DATABASE)
    cursor = connection.cursor()
    create_db('eco_guild_mgu', cursor)
    cursor.close()
    close_connection(connection)
