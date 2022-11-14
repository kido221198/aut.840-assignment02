import paho.mqtt.subscribe as subscribe
import time
import json
import endpoint as ep


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))


def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    topic = msg.topic.split("/")
    robot_id = topic[2]
    message = json.load(msg.payload)
    state = message['state']
    ts = string_to_epoch(message['time'])
    ep.save_telemetry(robot_id, ts, state)


def string_to_epoch(string):
    # year = int(string[0:4])
    # month = int(string[5:7])
    # day = int(string[8:10])
    # hour = int(string[11:13])
    # minute = int(string[14:16])
    # second = int(string[17:19])
    pattern = '%Y.%m.%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(string, pattern)))
    return epoch


def mqtt_client():
    print('MQTT is running...')
    # client = mqtt.Client("mqtt-runner")  # Create instance of client with client ID “digi_mqtt_test”
    # client.on_connect = on_connect
    # client.on_message = on_message
    #
    # client.connect("broker.hivemq.com", 1883, 60)  # Connect to (broker, port, keepalive-time)
    #
    # client.loop_forever()  # Start networking daemon

    subscribe.callback(on_message, "ii22/telemetry/+", hostname="broker.hivemq.com")
