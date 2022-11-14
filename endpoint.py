import repository as rp

EXIT_SUCCESS = False
EXIT_FAILURE = True


def get_latest_telemetry(robot_id):
    err, res = rp.get_current_value(robot_id)

    if err:
        return EXIT_FAILURE, None, None

    else:
        ts = res[0]
        value = res[1]
        return EXIT_SUCCESS, ts, value


def get_history(robot_id, start_ts, end_ts):
    err, res = rp.get_logged_values(robot_id, start_ts, end_ts)

    if err:
        return EXIT_FAILURE, None

    else:
        history = []

        for record in res:
            history.append({'ts': record[0], 'value': record[1]})

        return EXIT_SUCCESS, history


def save_telemetry(robot_id, ts, value):
    rp.save_value(robot_id, ts, value)
    return EXIT_SUCCESS


def save_alarm(robot_id, ts, content):
    rp.save_alarm(robot_id, ts, content)
    return EXIT_SUCCESS


def get_alarm_robot(robot_id, start_ts, end_ts):
    err, res = rp.get_alarm_by_robot(robot_id, start_ts, end_ts)

    if err:
        return EXIT_FAILURE, None

    else:
        log = []

        for record in res:
            log.append({'ts': record[0], 'value': record[1]})

        return EXIT_SUCCESS, log


def get_alarms(start_ts, end_ts):
    err, res = rp.get_all_alarm(start_ts, end_ts)

    if err:
        return EXIT_FAILURE, None

    else:
        log = []

        for record in res:
            log.append({'ts': record[0], 'robot_id': record[1], 'value': record[2]})

        return EXIT_SUCCESS, log


def check_robots():
    pass
