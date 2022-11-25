from common_var import TermColor, Logic
import sqlite3

con = None
cur = None


# CREATE TABLE robot (id STRING PRIMARY KEY, manufacturer STRING);
# CREATE TABLE currentValue (ts INTEGER, robot_id STRING PRIMARY KEY, value STRING);
# CREATE TABLE loggedValue (ts INTEGER, robot_id STRING, value STRING, PRIMARY KEY (ts, robot_id));
# CREATE TABLE alarm (ts INTEGER, robot_id STRING, value STRING, PRIMARY KEY (ts, robot_id));

def initialize():
    global con, cur
    con, cur = open_connection()
    # q1 = 'DELETE FROM currentValue;'
    # q2 = 'DELETE FROM loggedValue;'
    # q3 = 'DELETE FROM alarm;'
    # cur.execute(q1)
    # cur.execute(q2)
    # cur.execute(q3)
    # con.commit()


def open_connection():
    connection = sqlite3.connect("fastory.db", check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection):
    connection.close()


def validate_robot(robot_id):
    q = 'SELECT id FROM robot ' \
        'WHERE id = "' + robot_id + '";'
    cur.execute(q)

    if not cur.rowcount:
        return Logic['NOT_FOUND']

    else:
        return Logic['SUCCESS']


def get_current_value(robot_id):
    q = 'SELECT ts, value FROM currentValue ' \
        'WHERE robot_id = "' + robot_id + '";'
    cur.execute(q)

    if not cur.rowcount:
        return Logic['NOT_FOUND'], None

    else:
        res = dict(zip([col[0] for col in cur.description], cur[0]))
        return Logic['SUCCESS'], res


def get_current_values():
    q = 'SELECT * FROM currentValue;'
    cur.execute(q)

    if not cur.rowcount:
        return Logic['NOT_FOUND'], None

    else:
        res = dict(zip([col[0] for col in cur.description], cur[0]))
        return Logic['SUCCESS'], res


def get_logged_values(robot_id, start_ts, end_ts):
    q = 'SELECT ts, value FROM currentValue ' \
        'WHERE robot_id = "' + robot_id + '" ' \
        'AND ts BETWEEN ' + str(start_ts) + ' AND ' + str(end_ts) + ';'
    cur.execute(q)

    if not cur.rowcount:
        return Logic['NOT_FOUND'], None

    else:
        res = []

        for row in cur.fetchall():
            res.append(dict(zip([col[0] for col in cur.description], row)))

        return Logic['SUCCESS'], res


def get_alarm_by_robot(robot_id, start_ts, end_ts):
    q = 'SELECT ts, value FROM alarm ' \
        'WHERE robot_id = "' + robot_id + '" ' \
        'AND ts BETWEEN ' + str(start_ts) + ' AND ' + str(end_ts) + ';'
    cur.execute(q)

    if not cur.rowcount:
        return Logic['NOT_FOUND'], None

    else:
        res = []

        for row in cur.fetchall():
            res.append(dict(zip([col[0] for col in cur.description], row)))

        return Logic['SUCCESS'], res


def get_all_alarm(start_ts, end_ts):
    q = 'SELECT ts, robot_id, value FROM alarm ' \
        'WHERE ts BETWEEN ' + str(start_ts) + ' AND ' + str(end_ts) + ';'
    cur.execute(q)

    if not cur.rowcount:
        return Logic['NOT_FOUND'], None

    else:
        res = []

        for row in cur.fetchall():
            res.append(dict(zip([col[0] for col in cur.description], row)))

        return Logic['SUCCESS'], res


def save_value(robot_id, ts, value):
    # q1 = "UPDATE currentValue SET ts = {}, value = '{}' WHERE robot_id = '{}';".format(ts, value, robot_id)

    q1 = "REPLACE INTO currentValue (robot_id, ts, value) VALUES ('{}', {}, '{}');".format(robot_id, ts, value)
    q2 = "INSERT INTO loggedValue (robot_id, ts, value) VALUES ('{}', {}, '{}');".format(robot_id, ts, value)
    try:
        print(TermColor['BOLD'] + q1)
        print(TermColor['BOLD'] + q2)
        cur.execute(q1)
        cur.execute(q2)
        print(TermColor['WARNING'] + 'DB is executing..', end=' ')
        con.commit()
        print(TermColor['OK'] + 'Done!')
        return Logic['SUCCESS']

    except con.Error as err:
        print(TermColor['FAIL'] + 'SQLite error: %s' % (' '.join(err.args)))
        con.rollback()
        return Logic['UNKNOWN_ERROR']


def save_alarm(robot_id, ts, value):
    q = 'INSERT INTO loggedValue (robot_id, ts, value)' \
        'VALUES (' + robot_id + ', ' + ts + ', ' + value + ');'

    try:
        print(TermColor['BOLD'] + q)
        cur.execute(q)
        print(TermColor['WARNING'] + 'DB is executing..', end=' ')
        con.commit()
        print(TermColor['OK'] + 'Done!')
        return Logic['SUCCESS']

    except con.Error as err:
        print(TermColor['FAIL'] + 'SQLite error: %s' % (' '.join(err.args)))
        con.rollback()
        return Logic['UNKNOWN_ERROR']
