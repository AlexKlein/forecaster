"""
Util for creating db schema.

"""
import os

from psycopg2 import connect, DatabaseError

import settings as config


DATABASE_USER = config.DATABASES['PG']['USER']
DATABASE_PASSWORD = config.DATABASES['PG']['PASSWORD']
DATABASE_NAME = config.DATABASES['PG']['DATABASE']
DATABASE_HOST = config.DATABASES['PG']['HOST']
DATABASE_PORT = config.DATABASES['PG']['PORT']


def check_connect():
    try:
        conn = connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT)
        conn.autocommit = True
    except DatabaseError as e:
        print("You've got Database Error {}".format(e.pgerror))
        raise

    return conn


def commands_launcher(sql_file, conn):
    sql_commands = sql_file.split(';')
    cursor = conn.cursor()

    for command in sql_commands:
        try:
            cursor.execute(command)
        except DatabaseError as e:
            print("Command skipped: {}".format(e.pgerror))


def start_up():
    connection = check_connect()

    for path, dirs, files in os.walk(os.path.dirname(os.getcwd())):

        if path.find('migrations') > 0:

            for f in files:
                full_path = os.path.join(path, f)
                file = open(full_path, 'r', encoding='UTF-8')
                commands_launcher(file.read(), connection)
                file.close()

    connection.commit()
    connection.close()
