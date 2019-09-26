import fire

from api.run_api import start_up as start_api
from utils.db_migration import start_up as start_db


class Executor(object):
    @classmethod
    def start_api(cls, host='0.0.0.0', port=8080):
        start_db()
        start_api(host, port)


if __name__ == '__main__':
    fire.Fire(Executor)
