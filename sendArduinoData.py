import serial
import time
def main():
	arduino = serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=0.1)
	arduino.write(str.encode(" "))
	time.sleep(1)
	arduino.write(str.encode("f"))
	print("Wrote")
	time.sleep(3)
	#arduino.write(str.encode("s"))
	#print(arduino.readline())
	#print("Wrote")
	#time.sleep(3)
	#arduino.write(str.encode("\n"))
	#print("Wrote 2")
	#time.sleep(3)
if __name__ == "__main__":
	while True:
		try:
			main()
		except KeyboardInterrupt:
			break
