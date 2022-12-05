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
    current_ts = int(time() * 1000)

    if not end_ts or end_ts > current_ts:
        end_ts = current_ts

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

            if not sequence:
                sequence = prev_sequence + 1

            if prev_sequence and sequence > prev_sequence + 1:
                rp.save_alarm(robot_id, ts, 'Missed message(s)!')

            if value == 'DOWN':
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
    current_ts = int(time() * 1000)

    if not end_ts or end_ts > current_ts:
        end_ts = current_ts

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
    current_ts = int(time() * 1000)

    if not end_ts or end_ts > current_ts:
        end_ts = current_ts

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
    current_ts = int(time() * 1000)

    if not end_ts or end_ts > current_ts:
        end_ts = current_ts

    if not start_ts:
        start_ts = end_ts - DEFAULT_TIME_RANGE

    if not start_ts < end_ts:
        return Logic['CONFLICT'], None

    err, res = rp.get_logged_values(robot_id, start_ts, end_ts)

    if err:
        print(TermColor['FAIL'] + 'Endpoint error code:', str(err))
        return err, res

    else:
        summary = {'READY-IDLE-STARVED': {'time': 0, 'count': 0},
                   'READY-PROCESSING-EXECUTING': {'time': 0, 'count': 0},
                   'DOWN': {'time': 0, 'count': 0}}

        down_detected = False
        before_down_ts = 0
        mtbf = 0
        time_between_failures = []

        total_time = end_ts - res[0]['ts']
        res.reverse()
        prev_value = res[0]['value']
        prev_ts = res[0]['ts']
        summary[prev_value]['time'] += end_ts - prev_ts

        for i in range(1, len(res)):
            ts = res[i]['ts']
            value = res[i]['value']

            if prev_value != value:
                summary[value]['count'] += 1

            summary[value]['time'] += prev_ts - ts

            if prev_value == 'DOWN':
                down_detected = True
                before_down_ts = ts

            if value == 'DOWN' and down_detected:
                time_between_failures.append(before_down_ts - prev_ts)
                down_detected = False

            prev_value = value
            prev_ts = ts

        for state, data in summary.items():
            summary[state]['percentage'] = round(100 * data['time'] / total_time, 2)
            summary[state]['avg'] = 0

            if data['count'] > 0:
                summary[state]['avg'] = round(data['time'] / data['count'] / 1000, 2)

            summary[state]['time'] = round(data['time'] / 1000)

        if time_between_failures:
            for number in time_between_failures:
                mtbf += number/len(time_between_failures)

        summary['mtbf'] = round(mtbf/1000)

        return Logic['SUCCESS'], summary


