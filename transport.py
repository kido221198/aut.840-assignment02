from flask import Flask, render_template, request
import endpoint as ep
import json
import time
app = Flask(__name__)

OK = 200
INTERNAL_SERVER_ERROR = 500


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/telemetry/<robot_id>')
def telemetry(robot_id):  # put application's code here
    err, res = ep.get_latest_telemetry(robot_id)

    if err:
        return None, INTERNAL_SERVER_ERROR

    else:
        return json.dumps(res), OK


@app.route('/history/<robot_id>')
def history(robot_id):  # put application's code here
    current_ts = int(time.time())
    end_ts = request.args.get('start_ts', default=current_ts, type=int)
    default_start_ts = end_ts - 86400000
    start_ts = request.args.get('start_ts', default=default_start_ts, type=int)

    err, res = ep.get_history(robot_id, start_ts, end_ts)

    if err:
        return None, INTERNAL_SERVER_ERROR

    else:
        return json.dumps(res), OK


@app.route('/alarms')
def get_alarms():  # put application's code here
    current_ts = int(time.time())
    end_ts = request.args.get('start_ts', default=current_ts, type=int)
    default_start_ts = end_ts - 86400000
    start_ts = request.args.get('start_ts', default=default_start_ts, type=int)

    err, res = ep.get_alarms(start_ts, end_ts)

    if err:
        return None, INTERNAL_SERVER_ERROR

    else:
        return json.dumps(res), OK


@app.route('/alarm/<robot_id>')
def get_alarm(robot_id):
    current_ts = int(time.time())
    end_ts = request.args.get('start_ts', default=current_ts, type=int)
    default_start_ts = end_ts - 86400000
    start_ts = request.args.get('start_ts', default=default_start_ts, type=int)

    err, res = ep.get_alarm_robot(robot_id, start_ts, end_ts)

    if err:
        return None, INTERNAL_SERVER_ERROR

    else:
        return json.dumps(res), OK


def flask_server():
    print('Flask is running...')
    app.run(host='127.0.0.1', port='5000')
