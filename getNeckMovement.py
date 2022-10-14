import brainflow
from time import sleep
from brainflow.board_shim import BoardShim, BrainFlowInputParams
def getNeckEMG(board, boardId, channel):
	board.start_stream(4500)
	sleep(1)
	data = board.get_board_data()
	board.stop_stream()
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
	#board.config_board("n")
	#Serial Setup
	#Program
	try:
		sleep(1)
		neck = getNeckEMG(board, 1, 0)
		print("Value: ")
		print(neck)
		sleep(1)
		neck = getNeckEMG(board, 1, 2)
		print(neck)
	finally:
		board.release_session()
if __name__ == "__main__":
	main()
