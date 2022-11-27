from dotenv import dotenv_values
from connect_db import open_connection, close_connection

config = dotenv_values(".env")

USER = config['USER']
HOST = config['HOST']
PASSWORD = config['PASSWORD']
PORT = config['PORT']
DATABASE = config['DATABASE']

def create_table(cursor):
    users_simple_info = """
                        CREATE TABLE IF NOT EXISTS users_simple_info (
                            user_id VARCHAR(32) UNIQUE PRIMARY KEY,
                            username VARCHAR (50) UNIQUE NOT NULL,
                            first_name VARCHAR (32),
                            patronymic VARCHAR (32),
                            surname VARCHAR (32),
                            status VARCHAR (20) NOT NULL,
                            phone_number VARCHAR (20),
                            email VARCHAR (50),
                            vk VARCHAR (50),
                            drivers_license BOOL DEFAULT False,
                            carsharing BOOL DEFAULT False,
                            wanna_be_carshar BOOL DEFAULT False
                        );"""

    schoolkid_info = """
                     CREATE TABLE IF NOT EXISTS schoolkid_info (
                         user_id VARCHAR(32) UNIQUE PRIMARY KEY,
                         status VARCHAR (20) NOT NULL,
                         school VARCHAR (250),
                         grade INT,
                         CONSTRAINT fk_user_id
                              FOREIGN KEY (user_id)
                                   REFERENCES users_simple_info(user_id)
                                   ON DELETE CASCADE ON UPDATE CASCADE
                     );"""

    students_info = """
                    CREATE TABLE IF NOT EXISTS student_info (
                        user_id VARCHAR(32) UNIQUE PRIMARY KEY,
                        status VARCHAR (20) NOT NULL,
                        university VARCHAR (250),
                        department VARCHAR (250),
                        year_of_studying VARCHAR (32),
                        higher_education VARCHAR (50),
                        having_degree BOOL,
                        science_degree VARCHAR (50),
                        CONSTRAINT fk_user_id
                           FOREIGN KEY (user_id) 
                               REFERENCES users_simple_info (user_id)
                               ON DELETE CASCADE ON UPDATE CASCADE
                    );"""

    for sql_create_table in [users_simple_info, schoolkid_info, students_info]:
        cursor.execute(sql_create_table)
    print('sozdal_tbs')


if __name__ == '__main__':
    connection = open_connection(USER, PASSWORD, HOST, PORT, DATABASE)
    cursor = connection.cursor()
    create_table(cursor)
    cursor.close()
    close_connection(connection)
