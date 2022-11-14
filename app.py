from threading import Thread
import time
from repository import initialize
from mqtt_runner import mqtt_client
from transport import flask_server
from endpoint import check_robots


def timed_checking():
    print('Timer is running...')
    while True:
        time.sleep(60)
        print('Start checking robots...')
        check_robots()


if __name__ == "__main__":
    initialize()
    mqtt = Thread(target=mqtt_client, name='mqtt')
    transport = Thread(target=flask_server, name='transport')
    timer = Thread(target=timed_checking, name='timer')
    mqtt.start()
    transport.start()
    timer.start()



# timer.join()
