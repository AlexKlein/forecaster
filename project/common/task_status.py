"""
Description of the class for processing task statuses.

"""
import enum


class TaskStatus(enum.Enum):
    DONE = 'DONE'
    PENDING = 'PENDING'
    NOT_EXIST = 'NOT_EXIST'
