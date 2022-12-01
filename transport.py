import endpoint as ep
from common_var import TermColor, STATUS_CODE
from flask import Flask, render_template, request, redirect, url_for
from json import dumps
app = Flask(__name__)

host = '127.0.0.1'
port = '5000'


@app.route('/')
def index():  # put application's code here
    return redirect(url_for('robot_page'))


@app.route('/robot')
def robot_page():  # put application's code here
    host_ip = 'http://' + host + ':' + port
    return render_template('robot.html', host_ip=host_ip)


@app.route('/alarm')
def alarm_page():  # put application's code here
    return render_template('alarm.html')


@app.route('/api/analysis')
def analysis(robot_id):
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.historical_data(robot_id, start_ts, end_ts)
    return dumps(res), STATUS_CODE[err]


@app.route('/api/telemetries')
def telemetries():  # put application's code here
    err, res = ep.get_latest_telemetries()
    return dumps(res), STATUS_CODE[err]


@app.route('/api/telemetry/<robot_id>')
def telemetry(robot_id):  # put application's code here
    err, res = ep.get_latest_telemetry(robot_id)
    return dumps(res), STATUS_CODE[err]


@app.route('/api/history/<robot_id>')
def history(robot_id):  # put application's code here
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.get_history(robot_id, start_ts, end_ts)
    return dumps(res), STATUS_CODE[err]


@app.route('/api/alarms')
def get_alarms():  # put application's code here
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.get_alarms(start_ts, end_ts)
    return dumps(res), STATUS_CODE[err]


@app.route('/api/alarm/<robot_id>')
def get_alarm(robot_id):
    end_ts = request.args.get('end_ts', default=None, type=int)
    start_ts = request.args.get('start_ts', default=None, type=int)

    err, res = ep.get_alarm_robot(robot_id, start_ts, end_ts)
    return dumps(res), STATUS_CODE[err]


def flask_server():
    print(TermColor['OK'] + 'Flask is running...')
    app.run(host=host, port=port)
