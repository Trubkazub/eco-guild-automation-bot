from dotenv import dotenv_values
from connect_db import open_connection, close_connection

config = dotenv_values(".env")

USER = config['USER']
HOST = config['HOST']
PASSWORD = config['PASSWORD']
PORT = config['PORT']
DATABASE = config['DATABASE']

def create_table(cursor):
    users_simple_info = f'CREATE TABLE IF NOT EXISTS users_simple_info (' \
                        f'user_id VARCHAR(32) UNIQUE PRIMARY KEY,' \
                        f'username VARCHAR (50) UNIQUE NOT NULL,' \
                        f'first_name VARCHAR (32),' \
                        f'patronymic VARCHAR (32),' \
                        f'surname VARCHAR (32),' \
                        f'status VARCHAR (20) NOT NULL,' \
                        f'phone_number VARCHAR (20),' \
                        f'email VARCHAR (50),' \
                        f'vk VARCHAR (50),' \
                        f'drivers_license BOOL DEFAULT False,' \
                        f'carsharing BOOL DEFAULT False,' \
                        f'wanna_be_carshar BOOL DEFAULT False' \
                        f');'

    schoolkid_info = f'CREATE TABLE IF NOT EXISTS schoolkid_info (' \
                     f'user_id VARCHAR(32) UNIQUE PRIMARY KEY,' \
                     f'username VARCHAR (50) UNIQUE NOT NULL,' \
                     f'status VARCHAR (20) NOT NULL,' \
                     f'school VARCHAR (250),' \
                     f'grade INT,' \
                     f'CONSTRAINT fk_user_id' \
                     f'     FOREIGN KEY (user_id)' \
                     f'          REFERENCES users_simple_info(user_id)' \
                     f'          ON DELETE CASCADE ON UPDATE CASCADE' \
                     f');'

    students_info = f'CREATE TABLE IF NOT EXISTS student_info (' \
                    f'user_id VARCHAR(32) UNIQUE PRIMARY KEY,' \
                    f'username VARCHAR (50) UNIQUE NOT NULL,' \
                    f'status VARCHAR (20) NOT NULL,' \
                    f'university VARCHAR (250),' \
                    f'department VARCHAR (250),' \
                    f'year_of_studying VARCHAR (32),' \
                    f'higher_education VARCHAR (50),' \
                    f'having_degree BOOL,' \
                    f'science_degree VARCHAR (50),' \
                    f'CONSTRAINT fk_user_id' \
                    f'   FOREIGN KEY (user_id) ' \
                    f'       REFERENCES users_simple_info (user_id)' \
                    f'       ON DELETE CASCADE ON UPDATE CASCADE' \
                    f');'

    for sql_create_table in [users_simple_info, schoolkid_info, students_info]:
        cursor.execute(sql_create_table)
    print('sozdal_tbs')


if __name__ == '__main__':
    connection = open_connection(USER, PASSWORD, HOST, PORT, DATABASE)
    cursor = connection.cursor()
    create_table(cursor)
    cursor.close()
    close_connection(connection)
