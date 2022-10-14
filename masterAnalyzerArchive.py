from __future__ import division
from yahoofinancials import YahooFinancials
import yfinance as yf
from timeout_decorator import timeout
from time import sleep
import timeout_decorator
from ast import literal_eval
from operator import itemgetter
from termcolor import colored
fileList = ["stockData022621.txt", "stockData030121.txt", "stockData030221.txt", "stockData030321.txt", "stockData030421.txt", "stockData030521.txt", "stockData031021.txt", "stockData031521.txt", "stockData031621.txt", "stockData031721.txt", "stockData031921.txt", "stockData032321.txt", "stockData032421.txt", "stockData032521.txt", "stockData032621.txt", "stockData040621.txt", "stockData040821.txt", "stockData040921.txt", "stockData041221.txt", "stockData041321.txt", "stockData041421.txt", "stockData041521.txt", "stockData041621.txt", "stockData041921.txt", "stockData042021.txt", "stockData042121.txt", "stockData042221.txt", "stockData042921.txt", "stockData043021.txt", "stockData050521.txt", "stockData050621.txt", "stockData050721.txt", "stockData051121.txt", "stockData051221.txt", "stockData051321.txt", "stockData051421.txt", "stockData051721.txt", "stockData052021.txt", "stockData052421.txt", "stockData052521.txt", "stockData052621.txt", "stockData052721.txt", "stockData052821.txt", "stockData060121.txt", "stockData060221.txt", "stockData060321.txt", "stockData060421.txt", "stockData060721.txt", "stockData060821.txt", "stockData060921.txt", "stockData061021.txt", "stockData061121.txt", "stockData061421.txt", "stockData061521.txt", "stockData061621.txt", "stockData061721.txt", "stockData061821.txt", "stockData062121.txt", "stockData062221.txt", "stockData062321.txt", "stockData062421.txt", "stockData062521.txt", "stockData070121.txt"]
totalProfit = [["OMP", "RUBY"], ["ASLN", "KOSS", "NBLX", "SSP"], ["MIK", "OMP", "PHIO", "PLXP", "SSKN", "TACO"], ["USAK"], [], ["PLXP", "WTRH", "BSVN"], ["MESA"], ["BKEP", "CNTY", "FNKO", "INOD", "NNBR"], ["LIFE", "SEEL"], ["ARAV", "NEON", "PLXP", "STKS"], ["IMTE", "LTRPA", "TOUR"], ["STKS"], ["FNKO", "RAIL", "RCON"], ["CLMT", "FNKO", "RAIL", "RCON"], [], ["TH"], ["GROW"], ["FBIO", "GROW"], ["EKSO", "TH"], ["GROW"], ["AFMD"], ["INPX"], [], [], [], ["GBOX", "SGBX"], ["KLXE"], ["GBOX", "TUSK"], ["GALT"], [], ["ELTK", "KLXE"], ["YELL"], ["HBP", "KLXE"], ["STKS"], ["SOHO"], ["CPSS", "CRIS", "MOXC", "SIEN"], ["HYRE", "STKS"], [], ["PDSB"], ["PLXP"], [], ["SND", "VTNR"], ["VTNR"], ["MOSY", "VTNR"], [], ["SCYX", "WHLR"], ["MOSY"], [], ["MOSY"], ["GGAL"], ["ADMS", "PLXP"], [], ["DTEA", "JAKK"], [], ["PLXP"], [], [], ["ATRO", "CENX"], [], ["MOXC"], ["QIPT", "DRTT", "TGA"], ["QIPT"], []]
partialProfit = [["CGIX", "MGTA"], ["CPSS", "OMP"], ["CLMT", "USAK"], ["EYEN", "OSS", "STIM"], ["BSVN", "CRMD", "OTIC"], ["ADMS", "ASLN", "BIVI", "CRMD", "SND", "TAST", "FLNT", "VJET"], ["LTRPA", "MFIN", "TAST"], ["BKEPP", "CLPS", "MESA"], ["CWBR", "ERYP", "STKS", "USAK"], ["AFMD", "BASI", "BKEP", "CNTY", "FNKO", "NNBR", "TZOO"], ["CSCW", "GLYC", "INOD", "MMLP", "STKS"], ["RCON"], ["MYSZ", "SOHON"], ["CSCW", "IMAC", "TILE"], ["AWH", "CSCW", "IDRA"], ["GROW"], ["MDGS"], ["VNOM"], ["FBIO", "GTIM"], ["AFMD", "SCR"], [], ["BRY", "BTBT", "FBIO"], [], ["SOHON", "SOHOO"], ["WHLRP"], ["GEOS", "HBP", "WHLRP"], ["GBOX", "HBP", "TACO"], ["CNTY"], [], [], ["CVGI", "IMAC", "MOSY"], ["CVGI"], ["CYCN"], [], ["CPSS"], ["MITO"], ["CRMD", "ELOX", "MOXC", "NNBR"], ["ELTK", "MOSY"], [], [], ["TILE", "TZOO"], ["SOHON"], ["JAKK", "SCYX"], ["BEKPP", "ELTK", "FAT", "MESA", "QMCO", "SCYX", "SOHOB"], ["MOSY", "VTNR", "SOHON", "SOHOO", "TGA"], ["TGA"], ["ELTK", "APEN", "WHLRD"], ["QMCO"], ["SND", "STKS"], [], ["TACT", "STKS", "MMLP"], [], ["CRIS"], [], ["ICON"], ["FAT", "RCON"], [], ["BYR", "BSVN", "CAMP", "CTLP", "GTX", "KMPH", "QMCO", "SSP"], ["CVGI", "GTX", "SOHOO", "TACT"], ["BSVN"], ["OSW"], ["DRTT", "QMCO"], []]
sortByOptions = {"beta":0, "50DayAverage":1, "200DayAverage":2, "deviance":3, "float":4, "cVolume":5, "aVolume":6, "baRatio":7, "growth":8, "pbRatio":9, "mRatio":10, "rsi":11, "rVolume":12, "swing":13, "kst":15}
masterDataList = []
sortBy = str(input("Enter what you want to sort by seperated by commas and no spaces: "))
sortBy = sortBy.split(",")
for fileNumber in range(len(fileList)):
	print(str(fileNumber)+" : "+fileList[fileNumber])
try:
	startRange = int(input("Enter start date by number (lowest is 0): "))
except ValueError:
	startRange = 0
try:
	endRange = int(input("Enter end date by number (largest is "+str(len(fileList))+"): "))
except ValueError:
	endRange = len(fileList)
if (sortBy==["all"]):
	sortBy = ["beta", "deviance", "float", "baRatio", "pbRatio", "mRatio", "rsi", "rVolume", "swing", "kst"]
fileDataList = []
highTrend = []
lowTrend = []
middleTrend = []
for category in sortBy:
	highTrend.append(0)
	lowTrend.append(0)
	middleTrend.append(0)
e=0
for file in fileList[startRange:endRange]:
	with open("stockData/"+file, "r") as f:
		data = f.read()
	data = literal_eval(data)
	stockDataDict = {}
	for stockData in data:
		categoryList = []
		for category in sortBy:
			try:
				if (stockData[sortByOptions[category]]==""):
					stockData[sortByOptions[category]] = None
				categoryList.append(stockData[sortByOptions[category]])
			except IndexError:
				categoryList.append(None)
				pass
		stockDataDict.update({stockData[14]:categoryList})
	fileDataList.append(stockDataDict)
for dict in fileDataList:
	sortedList = []
	i=0
	month = str(fileList[e])[9:-8]
	day = str(fileList[e])[11:-6]
	year = str(fileList[e])[13:-4]
	print("\n\n\n\n"+month+"-"+day+"-"+year)
	#print("\n\n\n\n")
	for category in sortBy:
		try:
			sortedDict = sorted(dict.items(), key=lambda c: c[1][i], reverse=False)
			transList = []
			for stock in sortedDict:
				transList.append(stock[0])
			sortedList.append(transList)
			print("\n"+category.upper())
			sNumber = len(transList)
			z=0
			preMiddle = 0
			middle = 0
			postMiddle = 0
			for stock in transList:
				reprint = True
				for profitStock in totalProfit[e]:
					if (profitStock==stock):
						print(colored(stock, "green"), end=", ")
						reprint = False
						if (sNumber//3>z):
							preMiddle+=2
						elif ((sNumber//3)<=z and (sNumber//3)*2>=z):
							middle+=2
						elif ((sNumber//3)*2<z):
							postMiddle+=2
						break
				for profitStock in partialProfit[e]:
					if (profitStock==stock):
						print(colored(stock, "blue"), end=", ")
						reprint = False
						if (sNumber//3>z):
							preMiddle+=1
						elif ((sNumber//3)<=z and (sNumber//3)*2>=z):
							middle+=1
						elif ((sNumber//3)*2<z):
							postMiddle+=1
						break
				if (reprint):
					pass
					print(stock, end=", ")
				z+=1
			#print("\n"+str(len(totalProfit[e]))+"/"+str(len(transList)))
			if (preMiddle>postMiddle and preMiddle>middle):
				lowTrend[i]+=1
			elif (middle>preMiddle and middle>postMiddle):
				middleTrend[i]+=1
			elif (postMiddle>preMiddle and postMiddle>middle):
				highTrend[i]+=1
			print("\nLow: "+str(preMiddle)+"\nHigh: "+str(postMiddle)+"\nMiddle: "+str(middle))
		except TypeError:
			continue
		finally:
			i+=1
	masterDataList.append(sortedList)
	e+=1
y=0
for category in sortBy:
	if (highTrend[y]>lowTrend[y]+middleTrend[y]):
		print("\nTrend is growing stocks have higher "+category+" by "+str(highTrend[y]-middleTrend[y]-lowTrend[y]))
	elif (middleTrend[y]>highTrend[y]+lowTrend[y]):
		print("\nTrend: Growing stocks have medium "+category+" by "+str(middleTrend[y]-highTrend[y]-lowTrend[y]))
	elif (lowTrend[y]>highTrend[y]+middleTrend[y]):
		print("\nTrend is growing stocks have lower "+category+" by "+str(lowTrend[y]-middleTrend[y]-highTrend[y]))
	y+=1
