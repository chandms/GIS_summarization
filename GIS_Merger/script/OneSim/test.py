import os,sys,math, datetime
from collections import defaultdict

eventLogReportFile = sys.argv[1]
intervalTime = 1000
deviceName = "DM"
totalFiles = 0
	
downloadMessagesList = []

intervalList = {}
intervalCounter = intervalTime

with open(eventLogReportFile) as logFile:
	for lines in logFile:
		splitLine = lines.split(" ")
		if(float(splitLine[0]) >= int(intervalCounter)):
			intervalList[intervalCounter] = downloadMessagesList
			print intervalList[intervalCounter]
			intervalCounter += intervalTime
		if splitLine[1] == 'DE' and deviceName in splitLine[3]:
			downloadMessagesList.append(splitLine[4])
	intervalList[intervalCounter] = downloadMessagesList
	#print intervalList