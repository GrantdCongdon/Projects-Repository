import RPi.GPIO as gpio
import sys

from Adafruit_IO import MQTTClient
gpio.setmode(gpio.BOARD)
ADAFRUIT_IO_USERNAME = 'Yeloay'
ADAFRUIT_IO_KEY = '87324f6c2bf14a90ae1af3ff020a9cba'
FEED_ID1 = 'Servo1'
gpio.setup(12, gpio.OUT)
pwm=gpio.PWM(12, 50)
pwm.start(7.5)
def connect(client):
    print 'Connected to Adafruit IO! Listening for {0} changes...'.format(FEED_ID1)
    client.subscribe(FEED_ID1)
def disconnect(client):
    print 'Disconnected from Adafruit IO!'
    pwm.stop()
    gpio.cleanup()
    sys.exit(1)
def message(client, feed_id, payload):
    print 'Feed {0} recieved new value: {1}'.format(feed_id, payload)
    if feed_id=="Servo1":
        desiredPosition=float(payload)
        DC=5.0/9.0*(desiredPosition)+5
        pwm.ChangeDutyCycle(DC)
try:
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = connect
    client.on_message = message
    client.connect()
    client.loop_blocking()

except KeyboardInterrupt:
    client.on_disconnect = disconnect
