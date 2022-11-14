from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return 'Hello World!'


@app.route('/telemetry/<robot_id>')
def telemetry(robot_id):  # put application's code here
    return 'Hello World!'


@app.route('/history/<robot_id>')
def history(robot_id):  # put application's code here
    return 'Hello World!'


@app.route('/alarms')
def get_alarms():  # put application's code here
    return 'Hello World!'


@app.route('/alarm/<robot>')
def get_alarm():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
