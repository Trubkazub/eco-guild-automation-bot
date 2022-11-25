from connect_db import open_connection, close_connection

def create_table(cursor):
    sql_create_table = f'CREATE TABLE IF NOT EXISTS user_info (' \
                       f'user_id serial PRIMARY KEY,' \
                       f'username VARCHAR (50) UNIQUE NOT NULL,' \
                       f'first_name VARCHAR (32) NOT NULL,' \
                       f'patronymic VARCHAR (32),' \
                       f'surname VARCHAR (32) NOT NULL,' \
                       f'status VARCHAR (20) NOT NULL,' \
                       f'university VARCHAR(250),' \
                       f'department VARCHAR(250),' \
                       f'year_of_studying VARCHAR(32),' \
                       f'phone_number VARCHAR(20),' \
                       f'email VARCHAR(50),' \
                       f'vk VARCHAR(50),' \
                       f'drivers_license BOOL,' \
                       f'carsharing BOOL);'

    cursor.execute(sql_create_table)
    print('sozdaltb')


USER = 'postgres'
HOST = '127.0.0.1'
PASSWORD = 1234
PORT = 5432
DATABASE = 'eco_guild_mgu'

if __name__ == '__main__':
    connection = open_connection(USER, PASSWORD, HOST, PORT, DATABASE)
    cursor = connection.cursor()
    create_table(cursor)
    cursor.close()
    close_connection(connection)
