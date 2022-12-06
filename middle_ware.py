import math
from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'FAST-Lab'

host_address = '192.168.0.62'
port = 5000

ws_id = '10'
dest_url = 'http://' + host_address + ':' + str(port) + '/events'
ip_conveyor = 'http://192.168.' + ws_id + '.2'
ip_robot = 'http://192.168.' + ws_id + '.1'

mqtt_host = 'broker.hivemq.com'
mqtt_port = 8000
mqtt_topic = 'ii22/task1'

client = mqtt.Client()

list_events = {
    'conveyor': ['Z1_Changed', 'Z2_Changed', 'Z3_Changed', 'Z4_Changed', 'Z5_Changed'],
    'robot': ['PenChangeStarted', 'PenChangeEnded', 'DrawStartExecution', 'DrawEndExecution'],
}


@app.route('/subscribe_event/<string:target>/<string:event_id>')
def subscribe(target, event_id):
    subscribe_event(target, event_id)
    return 'Success', 200


@app.route('/unsubscribe_event/<string:target>/<string:event_id>')
def unsubscribe(target, event_id):
    unsubscribe_event(target, event_id)
    return 'Success', 200


@app.route('/events', methods=['POST'])
def event():
    payload = request.json
    print(payload)
    client.publish(mqtt_topic, payload=json.dumps(payload))
    return 'Success', 200


def subscribe_event(target, event_id):
    url = '/rest/events/' + event_id + '/notifs'

    if target == 'robot':
        url = ip_robot + url

    elif target == 'conveyor':
        url = ip_conveyor + url

    print('Sending request POST ' + url)
    print(requests.post(url, json={'destUrl': dest_url}))


def unsubscribe_event(target, event_id):
    url = '/rest/events/' + event_id + '/notifs'

    if target == 'robot':
        url = ip_robot + url

    elif target == 'conveyor':
        url = ip_conveyor + url

    print('Sending request DELETE ' + url)
    print(requests.delete(url, json={'destUrl': dest_url}))


def subscribe_all():
    for target, events in list_events.items():
        for event in events:
            subscribe(target, event)


if __name__ == '__main__':
    input_mqtt_host = input("Put in the IP of the MQTT Broker: ")
    input_mqtt_port = input("Put in the Port of the MQTT Broker: ")
    input_mqtt_topic = input("Put in the Topic of the MQTT Broker: ")

    if input_mqtt_host:
        mqtt_host = input_mqtt_host

    if input_mqtt_port and input_mqtt_port.isdigit():
        mqtt_port = input_mqtt_port

    if input_mqtt_topic:
        mqtt_topic = input_mqtt_topic

    subscribe_all()
    client.connect(mqtt_host, keepalive=60)
    client.publish(mqtt_topic, json.dumps({"script": "Hello World!"}))
    app.run(host=host_address, port=port)