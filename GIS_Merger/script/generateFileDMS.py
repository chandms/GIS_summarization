import sys,os
import datetime
import random
if ((len(sys.argv) < 3)):
    print """\
This script renames files inside the folder to the format accepted by DMS App

Usage:  python generateFileDMS.py latitude longitude SOURCE time_range dirName
1. Filename will be randomly spread in the area near latitude and longitude
2. Give SOURCE the same as given in DMS app
3. time_range : Time difference from the current time
4. dirName : Directory at which you want to rename the files


EXTENSION CONVERSION
---------------------
1. .webm -> .mp4

TYPE CONVERSION
---------------------
1. .jpg -> IMG
2. .mp4 -> VID
3. .webm -> VID
4. .txt -> SMS
"""
    sys.exit(1)


lat = float(sys.argv[1])
lon = float(sys.argv[2])
# noOfFiles = int(sys.argv[3])

#x_range = float(sys.argv[4])
#y_range = float(sys.argv[5])

TTL = 50
SOURCE = sys.argv[3]
time_range = int(sys.argv[4])

dirName = sys.argv[5]


type_list = ["Victim","Shelter","Food","Health"]


def genFile(fileName, size):
	with open(dirName + '/' + fileName, 'wb') as fout:
		fout.write(os.urandom(size * 1024 * 1024))

def getLatLong():
	val = random.randint(0,100)
	if val < 20:
		ddd = random.randint(1000,1500)
	else:
		ddd = random.randint(1500,2000)

	v = random.randint(0,3)
	if v == 0:
		la = float(lat - float(random.randint(0,ddd))/1000000.0)
		lo = float(lon + float(random.randint(0,ddd))/1000000.0)
	elif v==1:
		la = float(lat + float(random.randint(0,ddd))/1000000.0)
		lo = float(lon - float(random.randint(0,ddd))/1000000.0)
	elif v==2:
		la = float(lat + float(random.randint(0,ddd))/1000000.0)
		lo = float(lon + float(random.randint(0,ddd))/1000000.0)
	elif v==3:
		la = float(lat - float(random.randint(0,ddd))/1000000.0)
		lo = float(lon - float(random.randint(0,ddd))/1000000.0)
	
	la = "%2.6f"% (la,)
	lo = "%2.6f"% (lo,)
	print str(la) +  ',' + str(lo)
	return (la,lo)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def getTime():
	d2 = datetime.datetime.now()
	d1 = d2 - datetime.timedelta(hours=time_range)
	
	return random_date(d1, d2).strftime('%Y%m%d%H%M%S')


onlyfiles = [f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]


for file_name in onlyfiles:
	time_str = datetime.datetime.now()
	
	dt_aware = time_str.strftime('%Y%m%d%H%M%S')
	#print dt_aware

	la,lo = getLatLong()
	time_r = getTime()

	if(file_name[-3:] == "jpg"):
		ext_str = "_1.jpg"
		type_str = "IMG_"
	if(file_name[-3:] == "mp4"):
		ext_str = "_1.mp4"
		type_str = "VID_"
	if(file_name[-4:] == "webm"):
		ext_str = "_1.mp4" 
		type_str = "VID_"
	if(file_name[-3:] == "txt"):
		ext_str = "_1.txt" 
		type_str = "SMS_"

	fileName = type_str + str(TTL) + "_" + random.choice(type_list) + "_" + str(SOURCE) + "_defaultMcs_" + str(la) + "_" + str(lo) + "_" + time_r + ext_str	

	os.rename(os.path.join(dirName, file_name), os.path.join(dirName, fileName))


	#size = 	random.randint(x_range,y_range)
	#genFile(fileName,size)
#print allFileNames
