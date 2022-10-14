import brainflow
from time import sleep
from brainflow.board_shim import BoardShim, BrainFlowInputParams
def transpose(array):
	newArray = []
	for i in range(len(array[0])):
		transitionArray = []
		for e in range(len(array)):
			transitionArray.append(array[e][i])
		newArray.append(transitionArray)
	return newArray
def getTilt(board, boardId):
	board.start_stream(4500)
	sleep(1)
	data = board.get_board_data()
	board.stop_stream()
	channel = board.get_accel_channels(boardId)[1]
	#print(len(data))
	#print(len(data[0]))
	print(data[channel])
	tiltData = transpose(data)
	print(len(tiltData))
	sum=0
	values=0
	for value in data[channel]:
		if (value!=0):
			sum+=value
			values+=1
	tilt = sum/values
	return tilt
def main():
	#Board setup
	BoardShim.enable_dev_board_logger()
	params = BrainFlowInputParams()
	params.serial_port = "/dev/ttyACM0"
	params.file = "bioData.txt"
	board = BoardShim(1, params)
	board.prepare_session()
	board.config_board("n")
	#Serial Setup
	#Program
	try:
		sleep(1)
		tilt = getTilt(board, 1)
		print("Tilt: ")
		print(tilt)
	finally:
		board.release_session()
if __name__ == "__main__":
	main()

