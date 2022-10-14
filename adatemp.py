from Adafruit_IO import Client
import subprocess
import time
import os
aio = Client('87324f6c2bf14a90ae1af3ff020a9cba')
def get_temp():
    os.system("sudo modprobe w1-gpio")
    os.system("sudo modprobe w1-therm")
    time1 = time.strftime("%H:%M")
    os.chdir("/sys/bus/w1/devices/28-0000093bdc48")
    with open("w1_slave", "r") as file1:
        tempfile = file1.read()
    file1_line2 = tempfile.split("\n")[1]
    tempnumber = file1_line2.split(" ")[9]
    tempfirst = float(tempnumber[2:])
    tempfirst = tempfirst / 1000
    temp1 = float(tempfirst)
    temp1 = round(temp1, 2)
    os.chdir("/home/pi/python")
    return temp1
counter = 1
print 'Starting Loop'
while counter<10:
    temp = get_temp()
    aio.send('Temp1', temp)
    print 'data value sent=', temp
    counter=counter+1
    time.sleep(30)
print 'Finishing running loop'
print 'program finished'
