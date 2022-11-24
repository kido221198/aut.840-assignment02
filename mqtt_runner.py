import paho.mqtt.subscribe as subscribe
from datetime import datetime
import json
import endpoint as ep


class TermColor:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def on_message(client, userdata, msg):
    print(TermColor.BOLD + "Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    topic = msg.topic.split("/")
    robot_id = topic[2]
    message = json.loads(msg.payload)
    state = message['state']
    ts = string_to_epoch(message['time'])
    print(robot_id, state, ts)
    ep.save_telemetry(robot_id, ts, state)


def string_to_epoch(string):
    year = int(string[0:4])
    month = int(string[5:7])
    day = int(string[8:10])
    hour = int(string[11:13])
    minute = int(string[14:16])
    second = int(string[17:19])
    millisecond = int(string[20:23])
    epoch = int(datetime(year, month, day, hour, minute, second).strftime('%s')) * 1000 + millisecond
    return epoch


def mqtt_client():
    print(TermColor.OK + 'MQTT is running...')
    subscribe.callback(on_message, "ii22/telemetry/+", hostname="broker.hivemq.com")
