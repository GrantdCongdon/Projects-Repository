from Adafruit_IO import Client
aio = Client('87324f6c2bf14a90ae1af3ff020a9cba')
import time
distance = 1
print 'starting loop'
while distance < 10:
    aio.send('Sensor', distance)
    distance=distance+1
    time.sleep(10)
print 'finish running loop'
print 'program closing'
