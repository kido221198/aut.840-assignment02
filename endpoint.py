import repository as rp
from common_var import TermColor, Logic, DEFAULT_TIME_RANGE, SCANNING_PERIOD
from time import time


def get_latest_telemetry(robot_id):
    if rp.validate_robot(robot_id) is Logic['SUCCESS']:
        err, res = rp.get_current_value(robot_id)

        if err:
            print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

        return err, res

    else:
        return Logic['NOT_FOUND'], None


def get_latest_telemetries():
    err, res = rp.get_current_values()

    if err:
        print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

    return err, res


def get_history(robot_id, start_ts, end_ts):
    if not end_ts:
        end_ts = int(time()) * 1000

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return Logic['CONFLICT'], None

    if rp.validate_robot(robot_id) is Logic['SUCCESS']:
        err, res = rp.get_logged_values(robot_id, start_ts, end_ts)

        if err:
            print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

        return Logic['SUCCESS'], res

    else:
        return Logic['NOT_FOUND'], None


def save_telemetry(robot_id, ts, value, sequence):
    if not ts:
        ts = int(time()) * 1000

    if rp.validate_robot(robot_id) is Logic['SUCCESS']:
        err, res = rp.get_current_value(robot_id)

        if err:
            print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

        else:
            prev_sequence = res['sequence']

            if prev_sequence and sequence > prev_sequence + 1:
                rp.save_alarm(robot_id, ts, 'Missed message(s)!')

            if 'DOWN' in value:
                save_alarm(robot_id, ts + 1, 'Robot is down!')

            err = rp.save_value(robot_id, ts, value, sequence)

            if err:
                print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

            return err

    else:
        return Logic['NOT_FOUND']


def save_alarm(robot_id, ts, value):
    if not ts:
        ts = int(time()) * 1000

    if rp.validate_robot(robot_id) is Logic['SUCCESS']:
        err = rp.save_alarm(robot_id, ts, value)

        if err:
            print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

        return err

    else:
        return Logic['NOT_FOUND']


def get_alarm_robot(robot_id, start_ts, end_ts):
    if not end_ts:
        end_ts = int(time()) * 1000

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return Logic['CONFLICT'], None

    if rp.validate_robot(robot_id) is Logic['SUCCESS']:
        err, res = rp.get_alarm_by_robot(robot_id, start_ts, end_ts)

        if err:
            print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

        return err, res

    else:
        return Logic['NOT_FOUND'], None


def get_alarms(start_ts, end_ts):
    if not end_ts:
        end_ts = int(time()) * 1000

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return Logic['CONFLICT'], None

    err, res = rp.get_all_alarm(start_ts, end_ts)

    if err:
        print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

    return err, res


def check_robots():
    err, res = rp.get_current_values()
    # err, res = rp.get_current_value('rob1')

    if err:
        print(TermColor['FAIL'] + 'Endpoint error code:', str(err))
        return err

    else:
        # print(res)
        current_ts = int(time() * 1000)

        for record in res:
            diff = current_ts - record['ts']

            if diff > SCANNING_PERIOD and 'IDLE' in record['value']:
                save_alarm(record['robot_id'], current_ts, 'Idled too long!')

        return Logic['SUCCESS']


def historical_data(robot_id, start_ts, end_ts):
    if not end_ts:
        end_ts = int(time()) * 1000

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return Logic['CONFLICT'], None

    err, res = rp.get_logged_values(robot_id, start_ts, end_ts)

    if err:
        print(TermColor['FAIL'] + 'Endpoint error code:', str(err))

    else:
        pass
