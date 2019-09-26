"""
Util for launching multiprocess tasks for using API.

"""
from api import postgres_wrapper
from common.task_manager import TaskManager
from common.task_status import TaskStatus

from scripts.get_this_day_forecast import start_up as start_daily_fc
from scripts.get_weekly_forecast import start_up as start_weekly_fc


task_manager = TaskManager()
method_map = {
    "start_daily_fc": start_daily_fc,
    "start_weekly_fc": start_weekly_fc
}


def get_prev_task_desc(conn, method, user_name):
    query = f"""select distinct coalesce(max(task_status), 'UNDEFINED') as task_status,
                           coalesce(max(task_id), 'UNDEFINED') as task_id
                    from   fc_api_task_queue
                    where  method = '{method}' and
                           user_name = '{user_name}' and
                           task_status != 'DONE' and
                           task_status != 'NOT_EXIST'"""
    query_result = conn.execute_query(raw_sql=query)
    return str(query_result[0].get('task_status')), str(query_result[0].get('task_id'))


def upd_task_status(conn, task_status, method, user_name):
    update_query = f"""update fc_api_task_queue set task_status = '{task_status}'
                       where method = '{method}' and user_name = '{user_name}'"""
    conn.execute(raw_sql=update_query)


def ins_task(conn, task_id, user_name, method, task_status):
    insert_query = f"""insert into fc_api_task_queue (task_id, 
                                                      user_name, 
                                                      method, 
                                                      task_status) values ('{task_id}', 
                                                                           '{user_name}',
                                                                           '{method}', 
                                                                           '{task_status}')"""
    conn.execute(raw_sql=insert_query)


def start_task(**params):
    user_name = params.get('user_name')
    method = params.get('method')
    connection = postgres_wrapper.PostgresWrapper()
    task_status, task_id = get_prev_task_desc(connection, method, user_name)
    task_result = None

    if task_status == 'PENDING':
        task_status, task_result = task_manager.get_task_result(task_id)

        if task_status != TaskStatus.PENDING:
            upd_task_status(connection, str(task_status.value), method, user_name)

    if task_status == 'UNDEFINED':

        if params.get('param'):
            task_id = task_manager.create_task(method=method_map.get(method), **params.get('param'))
        else:
            task_id = task_manager.create_task(method=method_map.get(method))

        task_status, task_result = task_manager.get_task_result(task_id)
        ins_task(connection, task_id, user_name, method, str(task_status.value))

    connection.execute('commit')

    return {
        "status": str(task_status.value),
        "result": task_result
    }
