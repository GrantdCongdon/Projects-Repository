import serial
import time
def main():
	arduino = serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=0.1)
	arduino.write(str.encode(" "))
	time.sleep(1)
	while True:
		try:
			command = str(input("Enter command to send: "))
			arduino.write(str.encode(command))
			time.sleep(0.5)
		except KeyboardInterrupt:
			break
if __name__ == "__main__":
	main()
