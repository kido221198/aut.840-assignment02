import endpoint as ep
from common_var import TermColor, TIMEZONE_DIFF
from paho.mqtt import subscribe as subscribe
import paho.mqtt as mqtt
from datetime import datetime
from json import loads

# list_topics = [("ii22/telemetry/rob1", 1),
#                ("ii22/telemetry/rob2", 1),
#                ("ii22/telemetry/rob3", 1),
#                ("ii22/telemetry/rob4", 1),
#                ("ii22/telemetry/rob5", 1),
#                ("ii22/telemetry/rob6", 1),
#                ("ii22/telemetry/rob7", 1),
#                ("ii22/telemetry/rob8", 1),
#                ("ii22/telemetry/rob9", 1),
#                ("ii22/telemetry/rob10", 1)]


list_robots = ['rob1', 'rob2', 'rob3', 'rob4', 'rob5',
               'rob6', 'rob7', 'rob8', 'rob9', 'rob10']


def on_message(client, userdata, msg):
    try:
        topic = msg.topic.split("/")
        robot_id = topic[2]

        if robot_id in list_robots:
            print(TermColor['NORMAL'] + "Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
            message = loads(msg.payload)
            state = message['state']
            sequence = message['sequenceNumber']
            ts = string_to_epoch(message['time'])
            print("Content:", robot_id, state, ts)
            ep.save_telemetry(robot_id, ts, state, sequence)

    except Exception as e:
        print(e)


def string_to_epoch(string):
    year = int(string[0:4])
    month = int(string[5:7])
    day = int(string[8:10])
    hour = int(string[11:13])
    minute = int(string[14:16])
    second = int(string[17:19])
    millisecond = int(string[20:23])
    epoch = int(datetime(year, month, day, hour, minute, second).timestamp()) * 1000 + millisecond
    return epoch


# def mqtt_client(message='MQTT is running...'):
#     print(TermColor['OK'] + message)
    # try:
    #     client = mqtt.client.Client()
    #     client.connect(host="broker.hivemq.com", keepalive=300)
    #     client.subscribe(list_topics)
    #     client.on_message = on_message
    #     client.loop_forever()

    # subscribe.callback(on_message, "ii22/telemetry/+", hostname="broker.hivemq.com")
    # mqtt_client(message='Revoking MQTT runner...')
    # except Exception as e:
    #     mqtt_client(message='Revoking MQTT runner...')


def mqtt_client(message='MQTT is running...'):
    print(TermColor['OK'] + message)
    try:
        subscribe.callback(on_message, "ii22/telemetry/+", hostname="broker.hivemq.com")
    except Exception as e:
        mqtt_client(message='Revoking MQTT runner...')

