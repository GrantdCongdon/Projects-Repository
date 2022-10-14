import RPi.GPIO as gpio
from Adafruit_IO import MQTTClient
import sys
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
FEED_ID1='Bulb1'
gpio.setup(23, gpio.OUT)
gpio.output(23, gpio.LOW)
ADAFRUIT_IO_USERNAME = 'Yeloay'
ADAFRUIT_IO_KEY = '87324f6c2bf14a90ae1af3ff020a9cba'
def connected(client):
    print 'Connect to Adafruit IO! Listening for {0} changes...'.format(FEED_ID1)
    client.subscribe(FEED_ID1)
def disconnected(client):
    print 'Disconnected from Adafruit IO!'
    gpio.cleanup()
    sys.exit(1)
def message(client, feed_id, payload):
    print 'Feed {0} recieved new value: {1}'.format(feed_id, payload)
    if feed_id=='Bulb1' and payload=="ON":
        gpio.output(23, gpio.HIGH)
    if feed_id=='Bulb1' and payload=="OFF":
        gpio.output(23, gpio.LOW)
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect()
client.loop_blocking()
