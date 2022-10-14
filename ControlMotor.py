import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#first motor
motor1cl=16
motor1cu=5
GPIO.setup(motor1cl, GPIO.OUT)
GPIO.setup(motor1cu, GPIO.OUT)
#secound motor
motor2cl=12
motor2cu=4
GPIO.setup(motor2cl, GPIO.OUT)
GPIO.setup(motor2cu, GPIO.OUT)
#buttons of control
button1=13
button2=27

button3=18
count=0
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#create moving functions
def motorcl(pin1, pin2):
	GPIO.output(pin1, GPIO.HIGH)
	GPIO.output(pin2, GPIO.LOW)
	#time.sleep(t)
def motorcu(pin1, pin2):
	GPIO.output(pin1, GPIO.LOW)
	GPIO.output(pin2, GPIO.HIGH)
	#time.sleep(t)
def motoroff(pin1, pin2):
	GPIO.output(pin1, GPIO.HIGH)
	GPIO.output(pin2, GPIO.HIGH)

while True:
	input_state2=GPIO.input(27)
	input_state=GPIO.input(13)
	input_state3=GPIO.input(18)
	if (input_state3 == False):
		count=count+1
		#time.sleep(1)
		if (count>1):
			count=0
	elif (input_state == False and count==0):
		motorcl(motor1cl, motor1cu)
	elif (input_state2 == False and count==0):
		motorcl(motor2cl, motor2cu)
	elif (input_state == False and count==1):
		motorcu(motor1cl, motor1cu)
	elif (input_state2 == False and count==1):
		motorcu(motor2cl, motor2cu)
	else:
		motoroff(motor1cl, motor1cu)
		motoroff(motor2cl, motor2cu)
