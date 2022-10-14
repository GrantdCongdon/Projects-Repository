import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.OUT)
pwm=gpio.PWM(23, 50)
pwm.start(7.5)
time.sleep(5)
dc=5.0/90*90+5
pwm.ChangeDutyCycle(dc)
time.sleep(5)
pwm.stop()
gpio.cleanup()
