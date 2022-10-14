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
x=0
totalWin=0
totalLoser=0
contested=0
dataExists = 0
c1=0
c2=0
c3=0
c4=0
c5=0
c6=0
c7=0
c8=0
c9=0
def union(li1, li2, li3, li4, li5, li6, li7, li8, li9):
	finalList = list(set().union(li1, li2, li3, li4, li5, li6, li7, li8, li9))
	return finalList
for eachFile in fileList:
	print("\n"+eachFile)
	with open("stockData/"+eachFile, "r") as f:
		data = f.read()
	data = literal_eval(data)
	finalList1 = []
	stockList = []
	betaList = {}
	devList = {}
	floatList = {}
	mList = {}
	rVolumeList = {}
	rsiList = {}
	swingList = {}
	kstList = {}
	pbList = {}
	baList = {}
	for stockData in data:
		try:
			if (stockData[0]=="" or stockData[3]=="" or stockData[4]=="" or stockData[10]=="" or stockData[11]=="" or stockData[13]==""):
				continue
			else:
				betaList.update({stockData[14]:stockData[0]})
				devList.update({stockData[14]:stockData[3]})
				floatList.update({stockData[14]:stockData[4]})
				mList.update({stockData[14]:stockData[10]})
				rsiList.update({stockData[14]:stockData[11]})
				swingList.update({stockData[14]:stockData[13]})
				stockList.append(stockData[14])
		except (ValueError, IndexError):
			continue
	betaListS = sorted(betaList.items(), key=itemgetter(1), reverse=True)
	devListS = sorted(devList.items(), key=itemgetter(1), reverse=True)
	floatListS = sorted(floatList.items(), key=itemgetter(1), reverse=True)
	mListS = sorted(mList.items(), key=itemgetter(1), reverse=True)
	rsiListS = sorted(rsiList.items(), key=itemgetter(1), reverse=True)
	swingListS = sorted(swingList.items(), key=itemgetter(1), reverse=True)
	betaListF = []
	for stock in betaListS:
		betaListF.append(stock[0])
	middleTermBeta = len(betaListF)//2
	devListF = []
	for stock in devListS:
		devListF.append(stock[0])
	middleTermDev = len(devListF)//2
	floatListF = []
	for stock in floatListS:
		floatListF.append(stock[0])
	upperTermFloat = (len(floatListF)//3)*2
	middleTermFloat = len(floatListF)//2
	lowerTermFloat = len(floatListF)//3
	mListF = []
	for stock in mListS:
		mListF.append(stock[0])
	middleTermM = len(mListF)//2
	rsiListF = []
	for stock in rsiListS:
		rsiListF.append(stock[0])
	middleTermRsi = (len(rsiListF)//3)*2
	swingListF = []
	for stock in swingListS:
		swingListF.append(stock[0])
	upperTermSwing = (len(swingListF)//3)*2
	middleTermSwing = len(swingListF)//2
	for betaStock in betaListF[:middleTermBeta]:
		for floatStock in floatListF[lowerTermFloat:middleTermFloat]:
			for swingStock in swingListF[:middleTermSwing]:
				for devStock in devListF[:middleTermDev]:
					for rsiStock in rsiListF[:middleTermRsi]:
						for mStock in mListF[:middleTermM]:
							if (betaStock==floatStock and floatStock==swingStock and swingStock==devStock and devStock==rsiStock and rsiStock==mStock):
								finalList1.append(mStock)
	#BREAK
	finalList2 = []
	betaList = {}
	floatList = {}
	swingList = {}
	devList = {}
	rsiList = {}
	mList = {}
	"""for stockData in data:
		try:
			if (stockData[0]=="" or stockData[12]=="" or stockData[13]=="" or stockData[15]==""):
				continue
			else:
				betaList.update({stockData[14]:stockData[0]})
				rVolumeList.update({stockData[14]:stockData[12]})
				swingList.update({stockData[14]:stockData[13]})
				kstList.update({stockData[14]:stockData[15]})
				stockList.append(stockData[14])
		except (ValueError, IndexError):
			continue
	betaListS = sorted(betaList.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	swingListS = sorted(swingList.items(), key=itemgetter(1), reverse=True)
	kstListS = sorted(kstList.items(), key=itemgetter(1), reverse=True)
	betaListF = []
	for stock in betaListS:
		betaListF.append(stock[0])
	upperTermBeta = (len(betaListF)//3)*2
	lowerTermBeta = len(betaListF)//3
	rVolumeListF = []
	for stock in rVolumeListS:
		rVolumeListF.append(stock[0])
	upperTermRVolume = (len(rVolumeListF)//3)*2
	lowerTermRVolume = len(rVolumeListF)//3
	swingListF = []
	for stock in swingListS:
		swingListF.append(stock[0])
	upperTermSwing = (len(swingListF)//3)*2
	kstListF = []
	for stock in kstListS:
		kstListF.append(stock[0])
	upperTermKst = (len(kstListF)//3)*2
	for rVolumeStock in rVolumeListF[lowerTermRVolume:upperTermRVolume]:
		for betaStock in betaListF[lowerTermBeta:upperTermBeta]:
			for swingStock in swingListF[:upperTermSwing]:
				for kstStock in kstListF[:upperTermKst]:
					if (rVolumeStock==betaStock and betaStock==swingStock and swingStock==kstStock):
						finalList2.append(kstStock)"""
	#BREAK
	finalList3 = []
	rVolumeList = {}
	betaList = {}
	swingList = {}
	kstList = {}
	for stockData in data:
		try:
			if (stockData[0]=="" or stockData[3]=="" or stockData[4]=="" or stockData[10]=="" or stockData[12]=="" or stockData[13]==""):
				continue
			else:
				betaList.update({stockData[14]:stockData[0]})
				devList.update({stockData[14]:stockData[3]})
				floatList.update({stockData[14]:stockData[4]})
				mList.update({stockData[14]:stockData[10]})
				rVolumeList.update({stockData[14]:stockData[12]})
				swingList.update({stockData[14]:stockData[13]})
				stockList.append(stockData[14])
		except (ValueError, IndexError):
			continue
	betaListS = sorted(betaList.items(), key=itemgetter(1), reverse=True)
	devListS = sorted(devList.items(), key=itemgetter(1), reverse=True)
	floatListS = sorted(floatList.items(), key=itemgetter(1), reverse=True)
	mListS = sorted(mList.items(), key=itemgetter(1), reverse=True)
	rVolumeListS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	swingListS = sorted(swingList.items(), key=itemgetter(1), reverse=True)
	betaListF = []
	for stock in betaListS:
		betaListF.append(stock[0])
	middleTermBeta = (len(betaListF)//2)
	devListF = []
	for stock in devListS:
		devListF.append(stock[0])
	upperTermDev = (len(devListF)//3)*2
	middleTermDev = len(devListF)//2
	floatListF = []
	for stock in floatListS:
		floatListF.append(stock[0])
	upperTermFloat = (len(floatListF)//3)*2
	middleTermFloat = len(floatListF)//2
	mListF = []
	for stock in mListS:
		mListF.append(stock[0])
	middleTermM = len(mListF)//2
	rVolumeListF = []
	for stock in rVolumeListS:
		rVolumeListF.append(stock[0])
	upperTermRVolume = (len(rVolumeListF)//3)*2
	lowerTermRVolume = len(rVolumeListF)//3
	swingListF = []
	for stock in swingListS:
		swingListF.append(stock[0])
	upperTermSwing = (len(swingListF)//3)*2
	for betaStock in betaListF[:middleTermBeta]:
		for devStock in devListF[:middleTermDev]:
			for floatStock in floatListF[:middleTermFloat]:
				for mStock in mListF[:middleTermM]:
					for rVolumeStock in rVolumeListF[lowerTermRVolume:upperTermRVolume]:
						for swingStock in swingListF[:upperTermSwing]:
							if (betaStock==devStock and devStock==floatStock and floatStock==mStock and mStock==rVolumeStock and rVolumeStock==swingStock):
								finalList3.append(swingStock)
	#BREAK
	finalList4 = []
	betaList = {}
	devList = {}
	floatList = {}
	mList = {}
	rVolumeList = {}
	swingList = {}
	for stockData in data:
		try:
			if (stockData[4]=="" or stockData[7]=="" or stockData[9]=="" or stockData[11]==""):
				continue
			else:
				floatList.update({stockData[14]:stockData[4]})
				baList.update({stockData[14]:stockData[7]})
				pbList.update({stockData[14]:stockData[9]})
				rsiList.update({stockData[14]:stockData[11]})
		except (ValueError, IndexError):
			continue
	floatDictS = sorted(floatList.items(), key=itemgetter(1))
	baDictS = sorted(baList.items(), key=itemgetter(1), reverse=True)
	pbDictS = sorted(pbList.items(), key=itemgetter(1), reverse=True)
	rsiDictS = sorted(rsiList.items(), key=itemgetter(1), reverse=True)
	floatListF = []
	for stock in floatDictS:
		floatListF.append(stock[0])
	middleTermFloat = len(floatListF)//2
	baListF = []
	for stock in baDictS:
		baListF.append(stock[0])
	lowerTermBa = len(baListF)//3
	upperTermBa = (len(baListF)//3)*2
	pbListF = []
	for stock in pbDictS:
		pbListF.append(stock[0])
	lowerTermPb = len(pbListF)//3
	upperTermPb = (len(pbListF)//3)*2
	rsiListF = []
	for stock in rsiDictS:
		rsiListF.append(stock[0])
	middleTermRsi = len(rsiListF)//3
	for baStock in baListF[lowerTermBa:upperTermBa]:
		for rsiStock in rsiListF[:middleTermRsi]:
			for pbStock in pbListF[lowerTermPb:upperTermPb]:
				for floatStock in floatListF[:middleTermFloat]:
					if (baStock==rsiStock and rsiStock==pbStock and pbStock==floatStock):
						finalList4.append(floatStock)
	#BREAK
	finalList5 = []
	floatList = {}
	baList = {}
	pbList = {}
	rsiList = {}
	for stockData in data:
		try:
			if (stockData[4]=="" or stockData[7]=="" or stockData[10]=="" or stockData[12]==""):
				continue
			else:
				floatList.update({stockData[14]:stockData[4]})
				baList.update({stockData[14]:stockData[7]})
				mList.update({stockData[14]:stockData[10]})
				rVolumeList.update({stockData[14]:stockData[12]})
		except (ValueError, IndexError):
			continue
	floatDictS = sorted(floatList.items(), key=itemgetter(1))
	baDictS = sorted(baList.items(), key=itemgetter(1), reverse=True)
	mDictS = sorted(mList.items(), key=itemgetter(1), reverse=True)
	rVolumeDictS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	floatListF = []
	for stock in floatDictS:
		floatListF.append(stock[0])
	middleTermFloat = len(floatListF)//2
	baListF = []
	for stock in baDictS:
		baListF.append(stock[0])
	lowerTermBa = len(baListF)//3
	upperTermBa = (len(baListF)//3)*2
	mListF = []
	for stock in mDictS:
		mListF.append(stock[0])
	upperTermM = (len(mListF)//3)*2
	rVolumeListF = []
	for stock in rVolumeDictS:
		rVolumeListF.append(stock[0])
	lowerTermRVolume = len(rVolumeListF)//3
	upperTermRVolume = (len(rVolumeListF)//3)*2
	for mStock in mListF[:upperTermM]:
		for baStock in baListF[lowerTermBa:upperTermBa]:
			for floatStock in floatListF[:middleTermFloat]:
				for rVolumeStock in rVolumeListF[lowerTermRVolume:upperTermRVolume]:
					if (mStock==baStock and baStock==floatStock and floatStock==rVolumeStock):
						finalList5.append(rVolumeStock)
	#BREAK
	finalList6 = []
	mList = {}
	baStock = {}
	floatStock = {}
	rVolumeStock = {}
	for stockData in data:
		try:
			if (stockData[0]=="" or stockData[4]=="" or stockData[11]=="" or stockData[15]==""):
				continue
			else:
				betaList.update({stockData[14]:stockData[0]})
				floatList.update({stockData[14]:stockData[4]})
				rsiList.update({stockData[14]:stockData[11]})
				kstList.update({stockData[14]:stockData[15]})
				rVolumeList.update({stockData[14]:stockData[12]})
		except (ValueError, IndexError):
			continue
	betaDictS = sorted(betaList.items(), key=itemgetter(1), reverse=True)
	floatDictS = sorted(floatList.items(), key=itemgetter(1), reverse=False)
	rsiDictS = sorted(rsiList.items(), key=itemgetter(1), reverse=True)
	kstDictS = sorted(kstList.items(), key=itemgetter(1), reverse=True)
	rVolumeDictS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	betaListF = []
	for stock in betaDictS:
		betaListF.append(stock[0])
	upperTermBeta = (len(betaListF)//3)*2
	lowerTermBeta = len(betaListF)//3
	floatListF = []
	for stock in floatDictS:
		floatListF.append(stock[0])
	middleTermFloat = len(floatListF)//2
	rsiListF = []
	for stock in rsiDictS:
		rsiListF.append(stock[0])
	upperTermRsi = (len(rsiListF)//3)*2
	kstListF = []
	for stock in kstDictS:
		kstListF.append(stock[0])
	middleTermKst = len(kstListF)//2
	rVolumeListF = []
	for stock in rVolumeDictS:
		rVolumeListF.append(stock[0])
	middleTermRVolume = len(rVolumeListF)//2
	for betaStock in betaListF[lowerTermBeta:upperTermBeta]:
		for floatStock in floatListF[:middleTermFloat]:
			for kstStock in kstListF[middleTermKst:]:
				for rsiStock in rsiListF[:upperTermRsi]:
					for rVolumeStock in rVolumeListF[middleTermRVolume:]:
						if (betaStock==floatStock and floatStock==kstStock and kstStock==rsiStock and rsiStock==rVolumeStock):
							finalList6.append(rVolumeStock)
	#BREAK
	finalList7 = []
	betaList = {}
	floatList = {}
	kstList = {}
	rsiStock = {}
	rVolumeStock = {}
	for stockData in data:
		try:
			if (stockData[4]=="" or stockData[12]=="" or stockData[15]==""):
				continue
			else:
				floatList.update({stockData[14]:stockData[4]})
				rVolumeList.update({stockData[14]:stockData[12]})
				kstList.update({stockData[14]:stockData[15]})
				devList.update({stockData[14]:stockData[3]})
		except (ValueError, IndexError):
			continue
	floatDictS = sorted(floatList.items(), key=itemgetter(1), reverse=True)
	rVolumeDictS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	kstDictS = sorted(kstList.items(), key=itemgetter(1), reverse=True)
	devDictS = sorted(devList.items(), key=itemgetter(1), reverse=True)
	floatListF = []
	for stock in floatDictS:
		floatListF.append(stock[0])
	lowerTermFloat = len(floatListF)//3
	upperTermFloat = (len(floatListF)//3)*2
	rVolumeListF = []
	for stock in rVolumeDictS:
		rVolumeListF.append(stock[0])
	lowerTermRVolume = len(rVolumeListF)//3
	upperTermRVolume = (len(rVolumeListF)//3)*2
	kstListF = []
	for stock in kstDictS:
		kstListF.append(stock[0])
	lowerTermKst = len(kstListF)//3
	upperTermKst = (len(kstListF)//3)*2
	devListF = []
	for stock in devDictS:
		devListF.append(stock[0])
	upperTermDev = (len(devListF)//3)*2
	lowerTermDev = len(devListF)//3
	for floatStock in floatListF[lowerTermFloat:upperTermFloat]:
		for rVolumeStock in rVolumeListF[lowerTermRVolume:upperTermRVolume]:
			for kstStock in kstListF[lowerTermKst:upperTermKst]:
				for devStock in devListF[lowerTermDev:upperTermDev]:
					if (floatStock==rVolumeStock and rVolumeStock==kstStock and kstStock==devStock):
						finalList7.append(devStock)
	#BREAK
	finalList8 = []
	floatList = {}
	rVolumeList = {}
	kstList = {}
	devList = {}
	"""for stockData in data:
		try:
			if (stockData[0]=="" or stockData[3]=="" or stockData[4]=="" or stockData[12]==""):
				continue
			else:
				betaList.update({stockData[14]:stockData[0]})
				floatList.update({stockData[14]:stockData[3]})
				devList.update({stockData[14]:stockData[4]})
				rVolumeList.update({stockData[14]:stockData[12]})
		except (ValueError, IndexError):
			continue
	betaDictS = sorted(betaList.items(), key=itemgetter(1), reverse=True)
	floatDictS = sorted(floatList.items(), key=itemgetter(1), reverse=True)
	devDictS = sorted(devList.items(), key=itemgetter(1), reverse=True)
	rVolumeDictS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	betaListF = []
	for stock in betaDictS:
		betaListF.append(stock[0])
	middleTermBeta = (len(betaListF)//2)
	floatListF = []
	for stock in floatDictS:
		floatListF.append(stock[0])
	upperTermFloat = (len(floatListF)//3)*2
	lowerTermFloat = len(floatListF)//3
	devListF = []
	for stock in devDictS:
		devListF.append(stock[0])
	upperTermDev = (len(devListF)//3)*2
	lowerTermDev = len(devListF)//3
	rVolumeListF = []
	for stock in rVolumeDictS:
		rVolumeListF.append(stock[0])
	upperTermRVolume = (len(rVolumeListF)//3)*2
	lowerTermRVolume = len(rVolumeListF)//3
	for betaStock in betaListF[:middleTermBeta]:
		for devStock in devListF[lowerTermDev:upperTermDev]:
			for floatStock in floatListF[lowerTermFloat:upperTermFloat]:
				for rVolumeStock in rVolumeListF[lowerTermRVolume:upperTermRVolume]:
					if (betaStock==devStock and devStock==floatStock and floatStock==rVolumeStock):
						finalList8.append(rVolumeStock)"""
	#BREAK
	finalList9 = []
	betaList = {}
	devList = {}
	floatList = {}
	rVolumeList = {}
	for stockData in data:
		try:
			if (stockData[3]=="" or stockData[7]=="" or stockData[12]==""):
				continue
			else:
				devList.update({stockData[14]:stockData[3]})
				baList.update({stockData[14]:stockData[7]})
				rVolumeList.update({stockData[14]:stockData[12]})
		except (ValueError, IndexError):
			continue
	devDictS = sorted(devList.items(), key=itemgetter(1), reverse=True)
	baDictS = sorted(baList.items(), key=itemgetter(1), reverse=True)
	rVolumeDictS = sorted(rVolumeList.items(), key=itemgetter(1), reverse=False)
	devListF = []
	for stock in devDictS:
		devListF.append(stock[0])
	lowerTermDev = len(devListF)//3
	baListF = []
	for stock in baDictS:
		baListF.append(stock[0])
	lowerTermBa = len(baListF)//3
	upperTermBa = (len(baListF)//3)*2
	rVolumeListF = []
	for stock in rVolumeDictS:
		rVolumeListF.append(stock[0])
	lowerTermRVolume = len(rVolumeListF)//3
	upperTermRVolume = (len(rVolumeListF)//3)*2
	for devStock in devListF[:lowerTermDev]:
		for baStock in baListF[lowerTermBa:upperTermBa]:
			for rVolumeStock in rVolumeListF[lowerTermRVolume:upperTermRVolume]:
				if (devStock==baStock and baStock==rVolumeStock):
					finalList9.append(rVolumeStock)
	if (len(finalList1)>0):
		print("List 1")
		c1+=1
	if (len(finalList2)>0):
		print("List 2")
		c2+=1
	if (len(finalList3)>0):
		print("List 3")
		c3+=1
	if (len(finalList4)>0):
		print("List 4")
		c4+=1
	if (len(finalList5)>0):
		print("List 5")
		c5+=1
	if (len(finalList6)>0):
		print("List 6")
		c6+=1
	if (len(finalList7)>0):
		print("List 7")
		c7+=1
	if (len(finalList8)>0):
		print("List 8")
		c8+=1
	if (len(finalList9)>0):
		print("List 9")
		c9+=1
	finalList = union(finalList1, finalList2, finalList3, finalList4, finalList5, finalList6, finalList7, finalList8, finalList9)
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
print(c1)
print(c2)
print(c3)
print(c4)
print(c5)
print(c6)
print(c7)
print(c8)
print(c9)
