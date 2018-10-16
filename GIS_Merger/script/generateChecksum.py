import sys,os, hashlib

dirName = sys.argv[1]
allFiles = os.listdir(dirName)

hashDict = {}
#print allFiles
for filename in allFiles:
	with open(os.path.join(dirName,filename)) as f:
		sha1 = hashlib.sha1()
		sha1.update(f.read())
		hashDict[filename] = str(sha1.hexdigest())
		print hashDict[filename]


with open(dirName + "hashes.txt","w") as f:
	f.write(str(hashDict))
print hashDict