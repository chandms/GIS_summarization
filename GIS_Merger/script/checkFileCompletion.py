import sys,os, hashlib
import datetime



heatvals = ""

dirName = sys.argv[1]
hashFile = sys.argv[2]

hashDict = eval(open(hashFile).read())
allFiles = os.listdir(dirName)


validFiles = []

for filename in allFiles:
	with open(os.path.join(dirName,filename)) as f:
		sha1 = hashlib.sha1()
		sha1.update(f.read())

		#print filename[-3:]
		if filename[-3:] == 'bts' or filename[0:3] == 'Map':
			continue
		if hashDict[filename] == str(sha1.hexdigest()):
			validFiles.append(filename)
			print filename

diffHeat = {}
maxDiff = 0
# calculate max diff from oldest file
for files, hashstr in hashDict.items():
	splitFile = files.split("_")[7]
	diff = datetime.datetime.now() - datetime.datetime.strptime(splitFile, '%Y%m%d%H%M%S')
	# print diff.total_seconds()
	if float(diff.total_seconds()) > maxDiff:
		maxDiff = diff.total_seconds()



for files in validFiles:
	splitFile = files.split("_")[7]
	diff = datetime.datetime.now() - datetime.datetime.strptime(splitFile, '%Y%m%d%H%M%S')
	print diff.total_seconds()
	diffHeat[files] = diff.total_seconds()

for filename,difference in diffHeat.items():
	difference = difference/maxDiff
	difference = 1 - difference
	diffHeat[filename] = difference
	splitFile = filename.split("_")
	heatvals = heatvals + "[" + str(splitFile[5])  + ',' + splitFile[6] +',"' + str(difference * 1000) + "\"],"

heatstr = '''var addressPoints = [
%s
];''' % heatvals

with open('heatvals.js', 'w') as f:
	f.write(heatstr)