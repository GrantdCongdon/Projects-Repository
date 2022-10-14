import brainflow
from time import sleep
import serial
from brainflow.board_shim import BoardShim, BrainFlowInputParams
def getData(board, boardId):
	board.start_stream(4500)
	sleep(1)
	data = board.get_board_data()
	board.stop_stream()
	return data
def getTilt(data, board, boardId):
	channel = board.get_accel_channels(boardId)[1]
	sum = 0
	values = 0
	for value in data[channel]:
		if (value!=0):
			sum+=value
			values+=1
	tilt = sum/values
	return tilt
def getNeckEMG(data, board, boardId, channel):
	channel = board.get_emg_channels(boardId)[channel]
	sum=0
	values=0
	for value in data[channel]:
		if (value>0):
			sum+=value
			values+=1
		elif (value<0):
			sum+=value*-1
			values+=1
	emg = sum/values
	return emg
def driveWheelchair(direction, serialObject):
	if (direction=="forward"):
		serialObject.write(str.encode("f"))
	elif (direction=="backward"):
		serialObject.write(str.encode("b"))
	elif (direction=="right"):
		serialObject.write(str.encode("r"))
	elif (direction=="left"):
		serialObject.write(str.encode("l"))
	elif (direction=="stop"):
		serialObject.write(str.encode("s"))
	else:
		serialObject.write(str.encode("k"))
	return 0
def main():
	killSwitch = False
	#Board setup
	params = BrainFlowInputParams()
	params.serial_port = "/dev/ttyACM0"
	params.file = "bioData.txt"
	board = BoardShim(1, params)
	attempts = 0
	while (attempts<=3):
		try:
			board.prepare_session()
		except brainflow.board_shim.BrainFlowError:
			attempts+=1
			pass
	board.config_board("n")
	#Serial Setup
	arduino = serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=0.1)
	arduino.write(str.encode(" "))
	#baseline values
	sleep(1)
	arduino.write(str.encode("z"))
	sleep(1)
	print("Calibrating...")
	data = getData(board, 1)
	base = getTilt(data, board, 1)
	print("Done: "+str(base))
	#Program
	try:
		sleep(1)
		print("Program Ready")
		while (not killSwitch):
			data = getData(board, 1)
			tilt = getTilt(data, board, 1)-base
			print(tilt)
			neckRight = getNeckEMG(data, board, 1, 0)
			neckLeft = getNeckEMG(data, board, 1, 2)
			reset = arduino.readline()[2:-5]
			if (tilt>-0.5 and tilt<-0.35):
				print("Forward")
				driveWheelchair("forward", arduino)
			elif (neckRight>500):
				print("Left")
				driveWheelchair("right", arduino)
			elif (neckLeft>500):
				print("Right")
				driveWheelchair("left", arduino)
			elif (reset=="calibrate"):
				base = getTilt(board, 1)
			else:
				driveWheelchair("stop", arduino)
			sleep(0.5)
	except KeyboardInterrupt:
		killSwitch = True
	finally:
		board.release_session()
if __name__ == "__main__":
	main()

