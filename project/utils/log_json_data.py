"""
Util for logging json data, which backs from 2Gis API.

"""
from datetime import datetime

from flask import session
from psycopg2 import sql, connect, DatabaseError

import settings as config


DATABASE_USER = config.DATABASES['PG']['USER']
DATABASE_PASSWORD = config.DATABASES['PG']['PASSWORD']
DATABASE_NAME = config.DATABASES['PG']['DATABASE']
DATABASE_HOST = config.DATABASES['PG']['HOST']
DATABASE_PORT = config.DATABASES['PG']['PORT']


def get_user():
    auth = session.get('oauth_oauth_token')

    if auth:
        return auth.get('user')

    return None


def check_connect():
    try:
        conn = connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT
            )
    except DatabaseError as e:
        print("You've got Database Error {}".format(e.pgerror))
        raise

    return conn


def log_data(json_data, URL, extend):
    user = 'user_name'
    params = (
        datetime.now(),
        user,
        URL,
        extend,
        str(json_data)
    )
    connection = check_connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            sql.SQL(
                "insert into fc_api_logs (updated_at,author_login,url,parameters_dict,jsondata) "
                "values (%s, %s, %s, %s, %s)"
            ),
            params
        )
    except DatabaseError as e:
        print("You've got Database Error {}".format(e.pgerror))
        raise

    cursor.close()
    connection.commit()
    connection.close()
