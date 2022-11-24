from flask import Flask, render_template, request
import endpoint as ep
import json
app = Flask(__name__)

STATUS_CODE = {0: 200, 1: 409, 2: 404, 9: 500}


class TermColor:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/alarm')
def alarm_page():  # put application's code here
    return render_template('alarm.html')


@app.route('/api/telemetry/<robot_id>')
def telemetry(robot_id):  # put application's code here
    err, res = ep.get_latest_telemetry(robot_id)
    return json.dumps(res), STATUS_CODE[err]


@app.route('/api/history/<robot_id>')
def history(robot_id):  # put application's code here
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.get_history(robot_id, start_ts, end_ts)
    return json.dumps(res), STATUS_CODE[err]


@app.route('/api/alarms')
def get_alarms():  # put application's code here
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.get_alarms(start_ts, end_ts)
    return json.dumps(res), STATUS_CODE[err]


@app.route('/api/alarm/<robot_id>')
def get_alarm(robot_id):
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.get_alarm_robot(robot_id, start_ts, end_ts)
    return json.dumps(res), STATUS_CODE[err]


def flask_server():
    print(TermColor.OK + 'Flask is running...')
    app.run(host='127.0.0.1', port='5001')
