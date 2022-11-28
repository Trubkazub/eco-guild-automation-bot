import psycopg2
from dotenv import dotenv_values
from psycopg2 import Error
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

    def insert_into_simple_info(self):
        sql_insert_simple_info = """
            INSERT INTO users_simple_info 
                (user_id, username, first_name, patronymic, surname,
                status, phone_number, email, vk, drivers_license,
                carsharing, wanna_be_carshar )
                VALUES %s
            ON CONFLICT (user_id) DO NOTHING;
        """
        keys = ('user_id', 'username', 'first_name', 'patronymic', 'surname',
                'status', 'phone_number', 'email', 'vk', 'drivers_license',
                'carsharing', 'wanna_be_carshar')

        info = tuple(str(self.data_[key]) for key in keys)
        self.cursor.execute(sql_insert_simple_info, (info,))

    def insert_into_students_table(self):
        sql_insert_student_info = """
            INSERT INTO student_info
                (user_id, status, university, department, year_of_studying,
                higher_education, having_degree, science_degree)
                VALUES %s
            ON CONFLICT (user_id) DO NOTHING;
        """
        keys = ('user_id', 'status', 'university', 'department', 'year_of_studying',
                'higher_education', 'having_degree', 'science_degree')
        info = tuple(self.data_[key] for key in keys)
        self.cursor.execute(sql_insert_student_info, (info,))

    def insert_into_schoolkid_info(self):
        sql_insert_schoolkid_info = """
            INSERT INTO schoolkid_info 
                user_id, status, school, grade
                VALUES %s
            ON CONFLICT (user_id) DO NOTHING;
        """
        keys = ('user_id', 'status', 'school', 'grade')
        info = tuple(self.data_[key] for key in keys)
        self.cursor.execute(sql_insert_schoolkid_info, (info,))

    def inserterv2(self):
        self.insert_into_simple_info()
        if self.data_['status'] == 'student':
            self.insert_into_students_table()
        else:
            self.insert_into_schoolkid_info()


with Connect(config) as conn:
    cur = conn.cursor()
    user = Inserter(union_dict, cur)
    user.inserterv2()
