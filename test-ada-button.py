from Adafruit_IO import Client
import sys
import os
from Adafruit_IO import MQTTClient
ADAFRUIT_IO_USERNAME = 'Yeloay'
ADAFRUIT_IO_KEY = '87324f6c2bf14a90ae1af3ff020a9cba'
FEED_ID = 'test-button'
aio = Client('87324f6c2bf14a90ae1af3ff020a9cba')

def connect(client):
    client.subscribe(FEED_ID)
def disconnect(client):
    sys.exit(1)
def message(client, feed_id, payload):
    feed_id = str(feed_id)
    payload = int(payload)
    if feed_id=="test-button":
        print payload
try:
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = connect
    client.on_message = message
    client.connect()
    client.loop_blocking()
except KeyboardInterrupt:
    client.on_disconnect = disconnect
