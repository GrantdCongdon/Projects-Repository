from tkinter import *
#this program finaly turns a light on and off
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)
window=Tk()
window.title("start")
while True:
    input_state = GPIO.input(13)
    if (input_state == False):
        GPIO.output(16, GPIO.HIGH)
    else:
        GPIO.output(16, GPIO.LOW)
print("done")
GPIO.cleanup()
#works
