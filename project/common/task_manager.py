"""
Description of the class for multiprocessor command launch.

"""
import uuid
from concurrent.futures import ProcessPoolExecutor

import settings as config
from common.task_status import TaskStatus


MAX_WORKERS = config.PROCESS_POOL


class TaskManager:

    def __init__(self):
        self._pool = None
        self._tasks = {}

    @property
    def pool(self):

        if self._pool is not None:
            return self._pool

        self._pool = ProcessPoolExecutor(max_workers=MAX_WORKERS)
        return self._pool

    def create_task(self, method, **kwargs):
        future = self.pool.submit(method, **kwargs)
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = future
        return task_id

    def cancel_task(self, task_id):

        if self._tasks.get(task_id):
            return self._tasks.get(task_id).cancel()

    def get_task_result(self, task_id):
        future = self._tasks.get(task_id)

        if future is None:
            return TaskStatus.NOT_EXIST, None

        if future.done():
            del self._tasks[task_id]
            return TaskStatus.DONE, future.result()

        return TaskStatus.PENDING, None
