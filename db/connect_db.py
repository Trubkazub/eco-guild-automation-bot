import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def open_connection(USER, PASSWORD, HOST, PORT, DATABASE):
    connection = None
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)

    except (Exception, Error) as error:
        print('connection failed cuz of', error)
        connection.close()

    if connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection


def close_connection(connection):
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    pass
