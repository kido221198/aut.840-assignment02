import repository as rp
from time import time

SUCCESS = 0
CONFLICT = 1
NOT_FOUND = 2
UNKNOWN_ERROR = 9

DEFAULT_TIME_RANGE = 86400000


def get_latest_telemetry(robot_id):
    if rp.validate_robot(robot_id):
        err, res = rp.get_current_value(robot_id)
        return err, res

    else:
        return NOT_FOUND, None


def get_latest_telemetries():
    err, res = rp.get_current_values()
    return err, res


def get_history(robot_id, start_ts, end_ts):
    if not end_ts:
        end_ts = int(time())

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return CONFLICT, None

    if rp.validate_robot(robot_id):
        err, res = rp.get_logged_values(robot_id, start_ts, end_ts)
        return SUCCESS, res

    else:
        return NOT_FOUND, None


def save_telemetry(robot_id, ts, value):
    if not ts:
        ts = int(time())

    if rp.validate_robot(robot_id):
        err = rp.save_value(robot_id, ts, value)
        return err

    else:
        return NOT_FOUND


def save_alarm(robot_id, ts, value):
    if not ts:
        ts = int(time())

    if rp.validate_robot(robot_id):
        err = rp.save_alarm(robot_id, ts, value)
        return err

    else:
        return NOT_FOUND


def get_alarm_robot(robot_id, start_ts, end_ts):
    if not end_ts:
        end_ts = int(time())

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return CONFLICT, None

    if rp.validate_robot(robot_id):
        err, res = rp.get_alarm_by_robot(robot_id, start_ts, end_ts)
        return err, res

    else:
        return NOT_FOUND, None


def get_alarms(start_ts, end_ts):
    if not end_ts:
        end_ts = int(time())

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return CONFLICT, None

    err, res = rp.get_all_alarm(start_ts, end_ts)
    return err, res


def check_robots():
    pass
