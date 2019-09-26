"""
Util for checking user permissions by oAuth2.

"""
from api import postgres_wrapper


def get_user_flag(conn, user) -> dict:
    query = ("select distinct 1 as is_flag "
             "from   fc_user_roles " 
             "where  user_name = '{name}'".format(name=user))
    return conn.execute_query(raw_sql=query)


def get_permission(user):
    try:
        connection = postgres_wrapper.PostgresWrapper()
        permission_flag = get_user_flag(connection, user)

        if int(permission_flag[0].get('is_flag')) > 0:
            return True
        else:
            return False

    except Exception as e:
        print("You've got API connection error:", e)
        return False
