from repository import initialize
from mqtt_runner import mqtt_client
from transport import flask_server
from endpoint import check_robots
from common_var import TermColor
from threading import Thread
import time


def timed_checking():
    print(TermColor['OK'] + 'Timer is running...')
    while True:
        # Invoke scanning every 60 secs
        try:
            print(TermColor['WARNING'] + 'Start checking robots...', end=' ')
            err = check_robots()

            if not err:
                print(TermColor['OK'] + 'Done!')

        except Exception as e:
            print(TermColor['FAIL'] + str(e))

        finally:
            time.sleep(60)


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
