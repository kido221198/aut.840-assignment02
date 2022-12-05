from repository import initialize
from mqtt_runner import mqtt_client
from common_var import TermColor, STATUS_CODE
from threading import Thread
import endpoint as ep

from flask import Flask, render_template, request, redirect, url_for
from json import dumps
import time

# Running this app.py as the transport layer
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


@app.route('/api/analysis/<robot_id>')
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
    # app.run(host=host, port=port, debug=True, use_reloader=False)
    app.run(debug=True, use_reloader=False)


def timed_checking():
    print(TermColor['OK'] + 'Timer is running...')
    while True:
        # Invoke scanning every 60 secs
        try:
            print(TermColor['WARNING'] + 'Start checking robots...', end=' ')
            err = ep.check_robots()

            if not err:
                print(TermColor['OK'] + 'Done!')

        except Exception as e:
            print(TermColor['FAIL'] + str(e))

        finally:
            time.sleep(60)


if __name__ == "app" or __name__ == '__main__':
    # Open DB connection and Refresh tables
    initialize()

    # Create a thread to run MQTT subscriber
    mqtt = Thread(target=mqtt_client, name='mqtt')
    mqtt.start()

    # Create a thread to host Flask server
    transport = Thread(target=flask_server, name='transport')
    transport.start()

    # Create a thread to invoke robot scanning every 1 minute
    timer = Thread(target=timed_checking, name='timer')
    timer.start()

