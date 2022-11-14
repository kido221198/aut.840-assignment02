import sqlite3

EXIT_SUCCESS = False
EXIT_FAILURE = True

con = None
cur = None


def initialize():
    global con, cur
    con, cur = open_connection()


def open_connection():
    connection = sqlite3.connect("fastory.db")
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection):
    connection.close()


def validate_robot(robot_id):
    q = 'SELECT id FROM robot ' \
        'WHERE id = "' + robot_id + '";'
    res = cur.execute(q)

    if not res.fetchone():
        return EXIT_FAILURE

    else:
        return EXIT_SUCCESS


def get_current_value(robot_id):
    is_valid = validate_robot(robot_id)

    if is_valid:
        q = 'SELECT (ts, value) FROM currentValue ' \
            'WHERE robot_id = "' + robot_id + '";'
        res = cur.execute(q)
        return EXIT_SUCCESS, res.fetchone()

    else:
        return EXIT_FAILURE, None


def get_logged_values(robot_id, start_ts, end_ts):
    is_valid = validate_robot(robot_id)

    if is_valid:
        q = 'SELECT (ts, value) FROM currentValue ' \
            'WHERE robot_id = "' + robot_id + '" ' \
            'AND ts BETWEEN ' + start_ts + ' AND ' + end_ts + ';'
        res = cur.execute(q)
        return EXIT_SUCCESS, res.fetchall()

    else:
        return EXIT_FAILURE, None


def get_alarm_by_robot(robot_id, start_ts, end_ts):
    q = 'SELECT (ts, value) FROM alarm ' \
        'WHERE robot_id = "' + robot_id + '" ' \
        'AND ts BETWEEN ' + start_ts + ' AND ' + end_ts + ';'
    res = cur.execute(q)
    return EXIT_SUCCESS, res.fetchall()


def get_all_alarm(robot_id, start_ts, end_ts):
    q = 'SELECT (ts, robot_id, value) FROM alarm ' \
        'WHERE ts BETWEEN ' + start_ts + ' AND ' + end_ts + ';'
    res = cur.execute(q)
    return EXIT_SUCCESS, res.fetchall()


def save_value(robot_id, ts, value):
    q1 = 'UPDATE currentValue' \
         'SET ts = ' + ts + ', value = ' + value + \
         'WHERE robot_id = ' + robot_id + ';'
    q2 = 'INSERT INTO loggedValue (robot_id, ts, value)' \
         'VALUES (' + robot_id + ', ' + ts + ', ' + value + ');'
    cur.execute(q1)
    cur.execute(q2)
    con.commit()
    return EXIT_SUCCESS


def save_alarm(robot_id, ts, value):
    q = 'INSERT INTO loggedValue (robot_id, ts, value)' \
        'VALUES (' + robot_id + ', ' + ts + ', ' + value + ');'
    cur.execute(q)
    con.commit()
    return EXIT_SUCCESS
