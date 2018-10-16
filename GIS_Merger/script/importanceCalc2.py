import os,sys,math, datetime
csvFilePath = sys.argv[1]

allFilesDir = sys.argv[2]


totalFiles = 0
for files in os.listdir(allFilesDir):
	if files.endswith("tile") or files.endswith("json"):
		continue
	if files[0:3] == "Map" or files[0:2] == '15' or files[0:2] == '.sync':
		continue
	totalFiles += 1

currentDateTime = datetime.datetime.strptime("20170301183000","%Y%m%d%H%M%S")



def get_importance(listFiles, timecount):
	typeDict = {}
	# print(len(listFiles))
	this_total_files = 0
	for files in listFiles:
		# print(files)
		if files.endswith("tile") or files.endswith("json"):
			continue
		if files[0:3] == "Map" or files[0:2] == '15' or files[0:2] == '.sync':
			continue
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
		if files.endswith("tile") or files.endswith("json"):
			continue
		if files[0:4] == " Map" or files[0:2] == '15' or files[0:2] == '.sync':
			continue
		splitFile = files.split("_")

		Type = splitFile[2]
		proportion = float(typeDict[Type]) / float(totalFiles)


		inf = ((-1.0) * math.log(proportion))/math.log(2.0)
		# print "inf:" + str(inf)
		this_time = datetime.datetime.strptime(splitFile[7],"%Y%m%d%H%M%S")
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



csvFile = open(csvFilePath)

csvFile.readline()
print("Time, Importance, Age, Number of Files")
for l in csvFile.readlines():
	ttt = int(l.split(",")[0])

	a = ",".join(l.split(",")[6:])
	
	#print str(ttt)
	fileList = eval(a)

	if(type(fileList) == type("a")):
		fileList = eval(fileList)

	# print(fileList)
	# print("\n\n")
	get_importance(fileList, ttt)
