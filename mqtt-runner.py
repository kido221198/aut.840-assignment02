import paho.mqtt.client as mqtt
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
    ts = time.time()
    ep.save_telemetry(robot_id, ts, message)


client = mqtt.Client("mqtt_client")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect
client.on_message = on_message

client.connect("http://mqtt.innoway.vn", 1883, 60)  # Connect to (broker, port, keepalive-time)

client.loop_forever()  # Start networking daemon
