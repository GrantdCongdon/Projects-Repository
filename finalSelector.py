from __future__ import division
from yahoofinancials import YahooFinancials
import yfinance as yf
from timeout_decorator import timeout
from time import sleep
import timeout_decorator
from ast import literal_eval
from operator import itemgetter
from termcolor import colored
from os import listdir, chdir
x=0
totalWin=0
totalLoser=0
contested=0
dataExists = 0
def union(li):
	finalList = []
	for item in range(len(li)):
		finalList = list(set(finalList) | set(li[item]))
	return finalList
def checkData(data, indexes):
	for d in range(len(data)):
		for i in range(len(indexes)):
			if (data[d]=="" and d==indexes[i]):
				return False
	return True
def parseSorted(li):
	sList = []
	for stock in li:
		sList.append(stock[0])
	return sList
with open("stockData/allData.txt", "r") as f:
	allData = f.readlines()
totalProfit = literal_eval(allData[0])
partialProfit = literal_eval(allData[1])
chdir("stockData")
fileList = listdir()
fileList.remove("allData.txt")
fileList.remove(".DS_Store")
chdir("../")
fileList = sorted(fileList, reverse=False)
for eachFile in fileList:
	print("\n"+eachFile)
	with open("stockData/"+eachFile, "r") as f:
		data = f.read()
	data = literal_eval(data)
	stockList = []
	betaDict = {}
	devDict = {}
	floatDict = {}
	mDict = {}
	rVolumeDict = {}
	rsiDict = {}
	swingDict = {}
	kstDict = {}
	pbDict = {}
	baDict = {}
	macDict = {}
	for stockData in data:
		stockList.append(stockData[14])
	#Start Selector 1
	finalList1 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [0, 3, 4, 10, 11, 13])):
				continue
			else:
				stock = stockData[14]
				betaDict.update({stock:stockData[0]})
				devDict.update({stock:stockData[3]})
				floatDict.update({stock:stockData[4]})
				mDict.update({stock:stockData[10]})
				rsiDict.update({stock:stockData[11]})
				swingDict.update({stock:stockData[13]})
		except (ValueError, IndexError):
			continue
	betaListS = sorted(betaDict.items(), key=itemgetter(1), reverse=True)
	devListS = sorted(devDict.items(), key=itemgetter(1), reverse=True)
	floatListS = sorted(floatDict.items(), key=itemgetter(1), reverse=True)
	mListS = sorted(mDict.items(), key=itemgetter(1), reverse=True)
	rsiListS = sorted(rsiDict.items(), key=itemgetter(1), reverse=True)
	swingListS = sorted(swingDict.items(), key=itemgetter(1), reverse=True)
	betaList = parseSorted(betaListS)
	middleTermBeta = len(betaList)//2
	devList = parseSorted(devListS)
	middleTermDev = len(devList)//2
	floatList = parseSorted(floatListS)
	middleTermFloat = len(floatList)//2
	lowerTermFloat = len(floatList)//3
	mList = parseSorted(mListS)
	middleTermM = len(mList)//2
	rsiList = parseSorted(rsiListS)
	middleTermRsi = len(rsiList)//2
	swingList = parseSorted(swingListS)
	middleTermSwing = len(swingList)//2
	for betaStock in betaList[:middleTermBeta]:
		for devStock in devList[:middleTermDev]:
			for floatStock in floatList[lowerTermFloat:middleTermFloat]:
				for mStock in mList[:middleTermM]:
					for rsiStock in rsiList[:middleTermRsi]:
						for swingStock in swingList[:middleTermSwing]:
							if (betaStock==devStock and devStock==floatStock and floatStock==mStock and mStock==rsiStock and rsiStock==swingStock):
								finalList1.append(swingStock)
	betaDict = {}
	devDict = {}
	floatDict = {}
	mDict = {}
	rsiDict = {}
	swingDict = {}
	#Number 2
	finalList2 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [0, 3, 4, 10, 12, 13])):
				continue
			else:
				stock = stockData[14]
				betaDict.update({stock:stockData[0]})
				devDict.update({stock:stockData[3]})
				floatDict.update({stock:stockData[4]})
				mDict.update({stock:stockData[10]})
				rVolumeDict.update({stock:stockData[12]})
				swingDict.update({stock:stockData[13]})
		except (ValueError, IndexError):
			continue
	betaListS = sorted(betaDict.items(), key=itemgetter(1), reverse=True)
	devListS = sorted(devDict.items(), key=itemgetter(1), reverse=True)
	floatListS = sorted(floatDict.items(), key=itemgetter(1), reverse=True)
	mListS = sorted(mDict.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeDict.items(), key=itemgetter(1), reverse=False)
	swingListS = sorted(swingDict.items(), key=itemgetter(1), reverse=True)
	betaList = parseSorted(betaListS)
	middleTermBeta = len(betaList)//2
	devList = parseSorted(devListS)
	middleTermDev = len(devList)//2
	floatList = parseSorted(floatListS)
	middleTermFloat = len(floatList)//2
	mList = parseSorted(mListS)
	middleTermM = len(mList)//2
	rVolumeList = parseSorted(rVolumeListS)
	upperTermRVolume = (len(rVolumeList)//3)*2
	lowerTermRVolume = len(rVolumeList)//3
	swingList = parseSorted(swingListS)
	upperTermSwing = (len(swingList)//3)*2
	for betaStock in betaList[:middleTermBeta]:
		for devStock in devList[:middleTermDev]:
			for floatStock in floatList[:middleTermFloat]:
				for mStock in mList[:middleTermM]:
					for rVolumeStock in rVolumeList[lowerTermRVolume:upperTermRVolume]:
						for swingStock in swingList[:upperTermSwing]:
							if (betaStock==devStock and devStock==floatStock and floatStock==mStock and mStock==rVolumeStock and rVolumeStock==swingStock):
								finalList2.append(swingStock)
	betaDict = {}
	devDict = {}
	floatDict = {}
	mDict = {}
	rVolumeDict = {}
	swingDict = {}
	#Number 3
	finalList3 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [4, 7, 10, 12])):
				continue
			else:
				stock = stockData[14]
				floatDict.update({stock:stockData[4]})
				baDict.update({stock:stockData[7]})
				mDict.update({stock:stockData[10]})
				rVolumeDict.update({stock:stockData[12]})
		except (ValueError, IndexError):
			continue
	floatListS = sorted(floatDict.items(), key=itemgetter(1), reverse=True)
	baListS = sorted(baDict.items(), key=itemgetter(1), reverse=True)
	mListS = sorted(mDict.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeDict.items(), key=itemgetter(1), reverse=False)
	floatList = parseSorted(floatListS)
	middleTermFloat = len(floatList)//2
	baList = parseSorted(baListS)
	upperTermBa = (len(baList)//3)*2
	lowerTermBa = len(baList)//3
	mList = parseSorted(mListS)
	upperTermM = (len(mList)//3)*2
	rVolumeList = parseSorted(mList)
	upperTermRVolume = (len(rVolumeList)//3)*2
	lowerTermRVolume = len(rVolumeList)//3
	for floatStock in floatList[:middleTermFloat]:
		for baStock in baList[lowerTermBa:upperTermBa]:
			for mStock in mList[:upperTermM]:
				for rVolumeStock in rVolumeList[lowerTermRVolume:upperTermRVolume]:
					if (floatStock==baStock and baStock==mStock and mStock==rVolumeStock):
						finalList3.append(rVolumeStock)
	floatDict = {}
	baDict = {}
	mDict = {}
	rVolumeDict = {}
	#Start 4
	finalList4 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [0, 4, 11, 12, 15])):
				continue
			else:
				stock = stockData[14]
				betaDict.update({stock:stockData[0]})
				floatDict.update({stock:stockData[4]})
				rsiDict.update({stock:stockData[11]})
				rVolumeDict.update({stock:stockData[12]})
				kstDict.update({stock:stockData[15]})
		except (ValueError, IndexError):
			continue
	betaListS = sorted(betaDict.items(), key=itemgetter(1), reverse=True)
	floatListS = sorted(floatDict.items(), key=itemgetter(1), reverse=False)
	rsiListS = sorted(rsiDict.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeDict.items(), key=itemgetter(1), reverse=False)
	kstListS = sorted(kstDict.items(), key=itemgetter(1), reverse=True)
	betaList = parseSorted(betaListS)
	upperTermBeta = (len(betaList)//3)*2
	lowerTermBeta = len(betaList)//3
	floatList = parseSorted(floatListS)
	middleTermFloat = len(floatList)//2
	rsiList = parseSorted(rsiListS)
	upperTermRsi = (len(rsiList)//3)*2
	rVolumeList = parseSorted(rVolumeListS)
	middleTermRVolume = len(rVolumeList)//2
	kstList = parseSorted(kstListS)
	middleTermKst = len(kstList)//2
	for betaStock in betaList[lowerTermBeta:upperTermBeta]:
		for floatStock in floatList[:middleTermFloat]:
			for rsiStock in rsiList[:upperTermRsi]:
				for rVolumeStock in rVolumeList[middleTermRVolume:]:
					for kstStock in kstList[middleTermKst:]:
						if (betaStock==floatStock and floatStock==rsiStock and rsiStock==rVolumeStock and rVolumeStock==kstStock):
							finalList4.append(kstStock)
	betaDict = {}
	floatDict = {}
	rsiDict = {}
	rVolumeDict = {}
	kstDict = {}
	#Start 5
	finalList5 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [3, 7, 12])):
				continue
			else:
				stock = stockData[14]
				devDict.update({stock:stockData[3]})
				baDict.update({stock:stockData[7]})
				rVolumeDict.update({stock:stockData[12]})
		except (ValueError, IndexError):
			continue
	devListS = sorted(devDict.items(), key=itemgetter(1), reverse=True)
	baListS = sorted(baDict.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeDict.items(), key=itemgetter(1), reverse=False)
	devList = parseSorted(devListS)
	lowerTermDev = len(devList)//3
	baList = parseSorted(baListS)
	upperTermBa = (len(baList)//3)*2
	lowerTermBa = len(baList)//3
	rVolumeList = parseSorted(rVolumeListS)
	upperTermRVolume = (len(rVolumeList)//3)*2
	lowerTermRVolume = len(rVolumeList)//3
	for devStock in devList[:lowerTermDev]:
		for baStock in baList[lowerTermBa:upperTermBa]:
			for rVolumeStock in rVolumeList[lowerTermRVolume:upperTermRVolume]:
				if (devStock==baStock and baStock==rVolumeStock):
					finalList5.append(rVolumeStock)
	devDict = {}
	baDict = {}
	rVolumeDict = {}
	#Start 6
	finalList6 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [4, 7, 9, 11])):
				continue
			else:
				stock = stockData[14]
				floatDict.update({stock:stockData[4]})
				baDict.update({stock:stockData[7]})
				pbDict.update({stock:stockData[9]})
				rsiDict.update({stock:stockData[11]})
		except (ValueError, IndexError):
			continue
	floatListS = sorted(floatDict.items(), key=itemgetter(1), reverse=False)
	baListS = sorted(baDict.items(), key=itemgetter(1), reverse=True)
	pbListS = sorted(pbDict.items(), key=itemgetter(1), reverse=True)
	rsiListS = sorted(rsiDict.items(), key=itemgetter(1), reverse=True)
	floatList = parseSorted(floatListS)
	middleTermFloat = len(floatList)//2
	baList = parseSorted(baListS)
	upperTermBa = (len(baList)//3)*2
	lowerTermBa = len(baList)//3
	pbList = parseSorted(pbListS)
	upperTermPb = (len(pbList)//3)*2
	lowerTermPb = len(pbList)//3
	rsiList = parseSorted(rsiListS)
	middleTermRsi = len(rsiList)//2
	for floatStock in floatList[:middleTermFloat]:
		for baStock in baList[lowerTermBa:upperTermBa]:
			for pbStock in pbList[lowerTermPb:upperTermPb]:
				for rsiStock in rsiList[:middleTermRsi]:
					if (floatStock==baStock and baStock==pbStock and pbStock==rsiStock):
						finalList6.append(rsiStock)
	floatDict = {}
	baDict = {}
	pbDict = {}
	rsiDict = {}
	#Start 7
	finalList7 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [3, 4, 12, 13])):
				continue
			else:
				stock = stockData[14]
				devDict.update({stock:stockData[3]})
				floatDict.update({stock:stockData[4]})
				rVolumeDict.update({stock:stockData[12]})
				swingDict.update({stock:stockData[13]})
		except:
			continue
	devListS = sorted(devDict.items(), key=itemgetter(1), reverse=True)
	floatListS = sorted(floatDict.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeDict.items(), key=itemgetter(1), reverse=False)
	swingListS = sorted(swingDict.items(), key=itemgetter(1), reverse=True)
	devList = parseSorted(devListS)
	upperTermDev = (len(devList)//3)*2
	lowerTermDev = len(devList)//3
	floatList = parseSorted(floatListS)
	upperTermFloat = (len(floatList)//3)*2
	lowerTermFloat = len(floatList)//3
	rVolumeList = parseSorted(rVolumeListS)
	upperTermRVolume = (len(rVolumeList)//3)*2
	lowerTermRVolume = len(rVolumeList)//3
	swingList = parseSorted(swingListS)
	upperTermSwing = (len(swingList)//3)*2
	lowerTermSwing = len(swingList)//3
	for devStock in devList[lowerTermDev:upperTermDev]:
		for floatStock in floatList[lowerTermFloat:upperTermFloat]:
			for rVolumeStock in rVolumeList[lowerTermRVolume:upperTermRVolume]:
				for swingStock in swingList[lowerTermSwing:middleTermFloat]:
					if (devStock==floatStock and floatStock==rVolumeStock and rVolumeStock==swingStock):
						finalList7.append(swingStock)
	devDict = {}
	floatDict = {}
	rVolumeDict = {}
	swingDict = {}
	#Start 8
	finalList8 = []
	for stockData in data:
		try:
			if (not checkData(stockData, [0, 3, 4, 10, 11, 12, 13, 15])):
				continue
			else:
				stock = stockData[14]
				betaDict.update({stock:stockData[0]})
				devDict.update({stock:stockData[3]})
				floatDict.update({stock:stockData[4]})
				rsiDict.update({stock:stockData[11]})
				rVolumeDict.update({stock:stockData[12]})
				swingDict.update({stock:stockData[13]})
				kstDict.update({stock:stockData[15]})
				mDict.update({stock:stockData[10]})
		except:
			continue
	for stock in betaDict:
		try:
			if ():
				finalList8.append(stock)
		except KeyError:
			continue
	#if (len(rVolumeList)>1 and len(floatList)>1 and len(kstList)>1 and rVolumeList[(len(rVolumeList)-1)//2]==floatList[(len(floatList)-1)//2] and floatList[(len(floatList)-1)//2]==kstList[(len(kstList)-1)//2] and len(stockList)>1):
	#	finalList8 = [rVolumeList[(len(rVolumeList)-1)//2]]
	#elif (len(stockList)>2 and len(betaList)>2 and len(mList)>2 and betaList[(len(betaList)-1)//2]==mList[(len(mList)-1)//2]):
	#	finalList8 = [betaList[(len(betaList)-1)//2]]
	#if (len(rVolumeList)>0):
	#	finalList8 = [rVolumeList[(len(rVolumeList)-1)//2]]
	devDict = {}
	floatDict = {}
	rVolumeDict = {}
	if (len(finalList1)>0):
		print("List 1")
	if (len(finalList2)>0):
		print("List 2")
	if (len(finalList3)>0):
		print("List 3")
	if (len(finalList4)>0):
		print("List 4")
	if (len(finalList5)>0):
		print("List 5")
	if (len(finalList6)>0):
		print("List 6")
	if (len(finalList7)>0):
		print("List 7")
	if (len(finalList8)>0):
		print("Print 8")
	finalList = union([finalList1, finalList2, finalList3, finalList4, finalList5, finalList6, finalList7, finalList8])
	if (stockList!=[]):
		dataExists+=1
	else:
		x+=1
		continue
	finalList = finalList[:3]
	winner=0
	loser=0
	print("")
	for stock in finalList:
		reprint = True
		for profitStock in totalProfit[x]:
			if (stock==profitStock):
				print(colored(stock, "green"), end=", ")
				reprint = False
				winner+=1
				break
		for partialStock in partialProfit[x]:
			if (stock==partialStock):
				print(colored(stock, "blue"), end=", ")
				reprint = False
				winner+=1
				break
		if (reprint):
			print(colored(stock, "red"), end=", ")
			loser+=1
	if (len(totalProfit[x])==0 and len(partialProfit[x])==0):
		print(colored("No Profitable Stocks", "red"))
	if (winner>loser):
		totalWin+=1
	elif (loser>winner):
		totalLoser+=1
	elif (winner==loser and winner!=0):
		contested+=1
	x+=1
print("\n\n"+str(totalWin)+" winner(s)")
print(str(totalLoser)+" loser(s)")
print(str(contested)+" contested")
print("Out of a total of "+str(totalWin+totalLoser+contested)+" trading days")
print("and a total of "+str(dataExists)+" days")
