import os,sys,math,datetime,copy
from collections import defaultdict,OrderedDict

eventGenFile = sys.argv[1]
eventLogReportFile = sys.argv[2]
intervalTime = int(sys.argv[3]) # in milli-seconds
deviceName = str(sys.argv[4])

totalFiles = 0

messageDict = defaultdict(list)


currentDateTime = datetime.datetime.strptime("20170330183000","%Y%m%d%H%M%S")

with open(eventGenFile) as f:
	for lines in f:
		splitLine = lines.split(" ")
		messageDict[splitLine[2]].append(splitLine[8])
		messageDict[splitLine[2]].append(splitLine[9].replace("\n",""))
		totalFiles += 1
	totalFiles += 11
	
downloadMessagesList = []

intervalList = {}
intervalCounter = intervalTime

with open(eventLogReportFile) as logFile:
	for lines in logFile:
		splitLine = lines.split(" ")

		# copy to interval list on each interval Counter
		if(float(splitLine[0]) >= int(intervalCounter)):
			# copy by value
			intervalList[intervalCounter] = copy.deepcopy(downloadMessagesList)
			intervalCounter += intervalTime
		# do only for message delivered
		if splitLine[1] == 'DE' and deviceName in splitLine[3]:
			downloadMessagesList.append(splitLine[4])
	intervalList[intervalCounter] = copy.deepcopy(downloadMessagesList)

print "Interval Dict : "+ str(intervalList)
print "****************************************************"

for intervals,messages in intervalList.iteritems():
	for messageId in range(len(messages)):
		mId = intervalList[intervals][messageId]
		if mId in messageDict:
			intervalList[intervals][messageId] = str(mId) + "_" + str(messageDict[mId][0]) + "_" + str(messageDict[mId][1])


def get_importance(listFiles, timecount):
	typeDict = {}
	# print(len(listFiles))
	this_total_files = 0
	for files in listFiles:
		this_total_files += 1
		splitFile = files.split("_")
		# print splitFile
		Type = splitFile[2]
		if Type in typeDict:
			typeDict[Type] += 1
		else:
			typeDict[Type] = 1
	if this_total_files == 0:
		print(str(timecount) + ", 0, 0, 0")
		# print "Importance : 0"
		# print "Age : 0"
		return

	totalImportance = 0
	totalTime = 0

	for files in listFiles:
		splitFile = files.split("_")

		Type = splitFile[2]
		proportion = float(typeDict[Type]) / float(totalFiles)


		inf = ((-1.0) * math.log(proportion))/math.log(2.0)
		# print "inf:" + str(inf)
		this_time = datetime.datetime.strptime(splitFile[1],"%Y%m%d%H%M%S")
		timeDiff = currentDateTime - this_time
		#if timeDiff.total_seconds()	< 0:
		#	print files + ' ' + str(timeDiff.total_seconds())
		#print "TimeDiff:" + str(timeDiff.total_seconds())
		importance = inf * math.pow(2.71828,-1.0 * float(timeDiff.total_seconds() / 3600.0 / 24))
		# print "%0.15f"% importance
		totalImportance += importance
		totalTime += timeDiff.total_seconds() / 60
		# print(this_total_files)



	# print "Importance :" + str(totalImportance/this_total_files)
	# print "Age : " + str(totalTime)
	print(str(timecount) + ", " + str(totalImportance/this_total_files) + "," + str(totalTime) + ", " + str(this_total_files))

od = OrderedDict(sorted(intervalList.items()))
print str(intervalList)

print "****** IMPORTANCE AND AGE CALCULATION *****"	
for intervals,messages in intervalList.iteritems():
	get_importance(messages,intervals)
