from threading import Thread
import time
from repository import initialize, close_connection
from mqtt_runner import mqtt_client
from transport import flask_server
from endpoint import check_robots


def timed_checking():
    print('Timer is running...')
    while True:
        # Invoke scanning every 60 secs
        time.sleep(60)
        print('Start checking robots...')
        check_robots()


if __name__ == "__main__":
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



# timer.join()
