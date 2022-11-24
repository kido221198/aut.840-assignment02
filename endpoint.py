import repository as rp
from time import time

SUCCESS = 0
CONFLICT = 1
NOT_FOUND = 2
UNKNOWN_ERROR = 9

DEFAULT_TIME_RANGE = 86400000


class TermColor:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_latest_telemetry(robot_id):
    if rp.validate_robot(robot_id) is SUCCESS:
        err, res = rp.get_current_value(robot_id)

        if err:
            print(TermColor.FAIL + 'Endpoint error code:', str(err))

        return err, res

    else:
        return NOT_FOUND, None


def get_latest_telemetries():
    err, res = rp.get_current_values()

    if err:
        print(TermColor.FAIL + 'Endpoint error code:', str(err))

    return err, res


def get_history(robot_id, start_ts, end_ts):
    if not end_ts:
        end_ts = int(time())

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return CONFLICT, None

    if rp.validate_robot(robot_id) is SUCCESS:
        err, res = rp.get_logged_values(robot_id, start_ts, end_ts)

        if err:
            print(TermColor.FAIL + 'Endpoint error code:', str(err))

        return SUCCESS, res

    else:
        return NOT_FOUND, None


def save_telemetry(robot_id, ts, value):
    if not ts:
        ts = int(time())

    if rp.validate_robot(robot_id) is SUCCESS:
        err = rp.save_value(robot_id, ts, value)

        if err:
            print(TermColor.FAIL + 'Endpoint error code:', str(err))

        return err

    else:
        return NOT_FOUND


def save_alarm(robot_id, ts, value):
    if not ts:
        ts = int(time())

    if rp.validate_robot(robot_id) is SUCCESS:
        err = rp.save_alarm(robot_id, ts, value)

        if err:
            print(TermColor.FAIL + 'Endpoint error code:', str(err))

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

    if rp.validate_robot(robot_id) is SUCCESS:
        err, res = rp.get_alarm_by_robot(robot_id, start_ts, end_ts)

        if err:
            print(TermColor.FAIL + 'Endpoint error code:', str(err))

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

    if err:
        print(TermColor.FAIL + 'Endpoint error code:', str(err))

    return err, res


def check_robots():
    pass
