import brainflow
import time
import argparse
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
def transpose(array):
	newArray = []
	for i in range(len(array[0])):
		transitionArray = []
		for e in range(len(array)):
			transitionArray.append(array[e][i])
		newArray.append(transitionArray)
	return newArray
def main():
	BoardShim.enable_dev_board_logger()
	params = BrainFlowInputParams()
	params.serial_port = "/dev/ttyACM0"
	params.file = "bioData.txt"
	board = BoardShim(1, params)
	board.prepare_session()
	board.config_board("n")
	board.start_stream(4500)
	time.sleep(5)
	data = board.get_board_data()
	aData = board.get_accel_channels(1)
	board.stop_stream()
	board.release_session()
	#df = pd.DataFrame(data).transpose()
	data = transpose(data)
	print(data)
	#accChannels = board.get_accel_channels(1)
	#for c in accChannels:
	#	print(c)
	#	for i in df.transpose()[c]:
	#		print(i)
if __name__ == "__main__":
	main()
