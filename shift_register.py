import RPi.GPIO as GPIO
import time
import random
import picamera
camera = picamera.PiCamera()
camera.vflip = True
#from tkinter import *
#The responces to the input
function_text={'reset': 'Function Complied', 'version1': 'Function Complied',
               'version2':'Function Complied', 'version3':'Function Complied',
               'version4':'Function Complied', 'versionx': 'Function Complied although it will malfunction'}
#set the basics up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#important varaibles
ser=4
rclk=13
srclk=21
srclr=25
escape=20
count=1
pin_n=16
num=pin_n+1
t=0
#use the important variables to set up the ic chip
GPIO.setup(ser, GPIO.OUT)
GPIO.setup(srclk, GPIO.OUT)
GPIO.setup(rclk, GPIO.OUT)
GPIO.setup(srclr, GPIO.OUT)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(escape, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#try to do something with the ic chip
GPIO.output(srclk, GPIO.LOW)
GPIO.output(rclk, GPIO.LOW)
#set the next value
GPIO.output(ser, GPIO.HIGH)
#make serial clear high so that out isn't immediadly cleared
GPIO.output(srclr, GPIO.HIGH)
#make the homade variables
#attempts to reset all of the pins low
def reset():
    for b in range(1, num):
        set1(x=1)
        shift(0)
        update(0)
    return
#shifts the pins
def shift(t):
    GPIO.output(srclk, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(srclk, GPIO.LOW)
    return
#turns the stored date in the pins to outputs
def update(t):
    GPIO.output(rclk, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(rclk, GPIO.LOW)
    return
#these are different ways of setting the next pin ready for shift high or low
def set1(x):
    if (x==0):
        GPIO.output(ser, GPIO.HIGH)
    else:
        GPIO.output(ser, GPIO.LOW)
    return
def set2():
    input_state=GPIO.input(5)
    if (input_state == False):
        GPIO.output(ser, GPIO.HIGH)
    else:
        GPIO.output(ser, GPIO.LOW)
    return
def setx(s):
    if (s==1):
        GPIO.output(ser, GPIO.HIGH)
    elif (s==0):
        GPIO.output(ser, GPIO.LOW)
def allstep():
    input_state=GPIO.input(5)
    time.sleep(0.07)
    input_state2=GPIO.input(12)
    time.sleep(0.07)
    if (input_state== False):
        GPIO.output(ser, GPIO.HIGH)
        shift(0.01)
        time.sleep(0.01)
        update(0.01)
    elif (input_state2== False):
        GPIO.output(ser, GPIO.LOW)
        shift(0.01)
        time.sleep(0.01)
        update(0.01)
#Different ways of using the ic chip to do different things with the LEDs
def version(rt):
    reset()
def version1(rt):
    for i in range(1, 9):
        shift(0.05)
        set1(x=0)
        time.sleep(rt)
        update(0.05)
    time.sleep(3)
    reset()
    print("Done!")
    return
def version2(ta):
    global t
    n=-2
    while (t<=ta):
        shift(0.01)
        set1(x=n)
        time.sleep(0.06)
        update(0.01)
        n=n+1
        t=t+1
        if (n>=2):
            n=-3
    reset()
def version5(rt):
    loop=1
    ti=0
    while (loop<=10):
        for b in range(1, num):
            shift(0.03)
            set1(x=random.randint(0,1))
            time.sleep(rt)
            update(0.03)
            ti=ti+1
        b=1
        ti=0
        loop=loop+1
def version3(rt):
    for s in range(1, num):
        shift(0.01)
        set1(x=0)
        time.sleep(0.1)
        update(0.01)
    for e in range(1, num):
        shift(0.01)
        set1(x=1)
        time.sleep(0.1)
        update(0.01)
    print("Done!")
    reset()
def version4(rt):
    while True:
        while (rt<=8):
            allstep()
            if (GPIO.input(escape)==False):
                break
        if (GPIO.input(escape)==False):
            break
        reset()
        rt=1
#special version-only works on one 8 bit shift register-doesn't work right
def versionx(rt):
    global count
    global shift
    while True:
        for f in range(1, 8):
            shift(0.1)
            setx(s=count)
            time.sleep(0.01)
            update(0.01)
            count=0
        count=1
        for b in range(1, 7):
            shift(0.01)
            setx(s=count)
            time.sleep(0.01)
            count=0
        count=1
        update(0.1)
        for b2 in range(1, 6):
            shift(0.01)
            setx(s=count)
            time.sleep(0.01)
            count=0
        count=1
        update(0.1)
        for b3 in range(1, 5):
            shift(0.01)
            setx(s=count)
            time.sleep(0.01)
            count=0
        count=1
        update(0.1)
        for b4 in range(1, 4):
            shift(0.01)
            setx(s=count)
            time.sleep(0.01)
            count=0
        count=1
        update(0.1)
        for b5 in range(1, 3):
            shift(0.01)
            setx(s=count)
            time.sleep(0.01)
            count=0
        count=1
        update(0.1)
        for b6 in range(1, 2):
            shift(0.01)
            setx(s=count)
            time.sleep(0.01)
            count=0
        count=1
        update(0.01)
        shift =(0.01)
        set1(x=0)
        time.sleep(0.01)
        count=1
    reset2()
    return
#control center storage
function = {'reset': reset, 'version 1': version1, 'version 2': version2,
            'version 3': version3, 'version 4': version4, 'versionx': versionx}
#choose the version that you want to run
#ta=99
camera.start_preview()
version5(rt=0.01)
camera.stop_preview()
camera.close()
version(rt=0)
#reset all of the values
GPIO.cleanup()
