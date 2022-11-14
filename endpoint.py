import repository as rp

EXIT_SUCCESS = True;
EXIT_FAILURE = False;


def get_latest_telemetry(robot_id):
    ts, value = rp.get_current_value(robot_id)
    return EXIT_SUCCESS, ts, value


def get_history(robot_id, start_ts, end_ts):
    history = rp.get_logged_values(robot_id, start_ts, end_ts)
    return EXIT_SUCCESS, history


def save_telemetry(robot_id, ts, value):
    rp.save_value(robot_id, ts, value)
    return EXIT_SUCCESS


def get_alarm_robots(start_ts, end_ts):
    log = rp.get_alarm(start_ts, end_ts)
    return EXIT_SUCCESS, log


def get_alarm_robot(robot_id, start_ts, end_ts):
    alarm = rp.get_alarm()
    return EXIT_SUCCESS, alarm


def check_robots():
    pass
