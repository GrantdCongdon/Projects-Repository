import serial
import sys
from Adafruit_IO import MQTTClient
#setup
ADAFRUIT_IO_USERNAME = 'Yeloay'
ADAFRUIT_IO_KEY = '87324f6c2bf14a90ae1af3ff020a9cba'
FEED_ID = 'Pibot'
serialMsg = serial.Serial("/dev/ttyACM0", 9600)
def connect(client):
    print 'Connected to Adafruit IO! Listening for {0} changes...'.format(FEED_ID)
    client.subscribe(FEED_ID)
def disconnect(client):
    print 'Disconnected from Adafruit IO!'
    sys.exit(1)
def message(client, feed_id, payload):
    print 'Feed {0} recieved new value: {1}'.format(feed_id, payload)
    feed_id = str(feed_id)
    payload = int(payload)
    if feed_id=="Pibot" and payload==5:
        serialMsg.write("r1000\n")
        serialMsg.write("l1000\n")
        print 'Success'
    elif feed_id=="Pibot" and payload==13:
        serialMsg.write("r2000\n")
        serialMsg.write("l2000\n")
        print 'Success'
    elif feed_id=="Pibot" and payload==10:
        
        serialMsg.write("r1000\n")
        serialMsg.write("l1000\n")
        print 'Success'
    elif feed_id=="Pibot" and payload==8:
        serialMsg.write("r2000\n")
        serialMsg.write("l1000\n")
        print 'Success'
    elif feed_id=="Pibot" and payload==9:
        serialMsg.write("r1000\n")
        serialMsg.write("l2000\n")
        print 'Success'
    elif feed_id=="Pibot" and payload==1:
        serialMsg.write("r1500\n")
        serialMsg.write("l1500\n")
        print 'Success'

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = connect
client.on_message = message
client.connect()
client.loop_blocking()
client.on_disconnect = disconnect
