import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor1cl=16
motor1cu=5
GPIO.setup(motor1cl, GPIO.OUT)
GPIO.setup(motor1cu, GPIO.OUT)
motor2cl=12
motor2cu=4
GPIO.setup(motor2cl, GPIO.OUT)
GPIO.setup(motor2cu, GPIO.OUT)

def clMotor(pin1, pin2):
	GPIO.output(pin1, GPIO.HIGH)
	GPIO.output(pin2, GPIO.LOW)
	time.sleep(2)
def cuMotor(pin1, pin2):
	GPIO.output(pin1, GPIO.LOW)
	GPIO.output(pin2, GPIO.HIGH)
	time.sleep(2)
def offMotor(pin1, pin2):
	GPIO.output(motor1cl, GPIO.LOW)
	GPIO.output(motor2cu, GPIO.LOW)

cuMotor(motor1cl, motor1cu)
clMotor(motor1cl, motor1cu)
offMotor(motor1cl, motor1cu)
time.sleep(3)
clMotor(motor2cl, motor2cu)
cuMotor(motor2cl, motor2cu)
offMotor(motor2cl, motor2cu)
GPIO.cleanup()
print("done")