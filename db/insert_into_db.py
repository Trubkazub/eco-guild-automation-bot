import psycopg2
from dotenv import dotenv_values
from psycopg2 import Error, sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
config = dotenv_values(".env")


class Connect:
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(user=self.config['USER'],
                                               password=self.config['PASSWORD'],
                                               host=self.config['HOST'],
                                               port=self.config['PORT'],
                                               database=self.config['DATABASE'])

        except (Exception, Error) as error:
            print('connection failed cuz of', error)
            self.connection.close()

        if self.connection:
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('conn opened')
            return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print('conn closed')


class Inserter:
    def __init__(self, data_, cursor):
        self.data_ = data_
        self.cursor = cursor

    def inserter(self, table):
        self.cursor.execute("Select * FROM {} LIMIT 0".format(table))
        colnames = [desc[0] for desc in self.cursor.description]
        info = tuple(str(self.data_[key]) for key in colnames)

        self.cursor.execute(
            sql.SQL('INSERT INTO {} VALUES %s ON CONFLICT (user_id) DO NOTHING').format(sql.Identifier(table)), (info,)
        )

    def choose_table(self):
        self.inserter('users_simple_info')
        if self.data_['status'] == 'student':
            self.inserter('student_info')
        else:
            self.inserter('schoolkid_info')




if __name__ == '__main__':
    with Connect(config) as conn:
        cur = conn.cursor()
        user = Inserter(data, cur)
        user.choose_table()
