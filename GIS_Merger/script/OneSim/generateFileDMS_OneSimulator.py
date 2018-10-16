import sys,os
import datetime
import random

if ((len(sys.argv) < 9)):
    print """\
This script generate Event file suitable for the purpose of OneSimulator

Usage:  python generateFileDMS.py latitude longitude noOfMessages noOfDevices x_range y_range time_range stepSizeCounter
(Files will be created inside sync directory)

1. Filename will be randomly spread in the area near latitude and longitude and size will be in between x_range and y_range
2. SOURCE and DESTINATION of the messages will be randomly assigned
3. time_range : Time difference from the current time
4. stepSize : stepSize for OneSimulator
5. x_range : Minimum Size of File
6. y_range : Maximum Size of File
"""
    sys.exit(1)

lat = float(sys.argv[1])
lon = float(sys.argv[2])

noOfMessages = int(sys.argv[3])

noOfDevices = int(sys.argv[4])

x_range = float(sys.argv[5])
y_range = float(sys.argv[6])

time_range = int(sys.argv[7])

stepSizeCounter = float(sys.argv[8])


created = "C"

type_list = ["Victim","Shelter","Food","Health"]

def genFile(fileName, size):
	with open('sync/' + fileName, 'wb') as fout:
		fout.write(os.urandom(size * 1024 * 1024))

def getLatLong():
	val = random.randint(0,100)
	if val < 20:
		ddd = 2000

	else:
		ddd = 1500

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

messageCount = 1
i = 0
step_size = 0.0
while i < noOfMessages:
	source = random.randint(1,noOfDevices)
	destination = random.randint(1,noOfDevices)
	if source != destination:
		time_str = datetime.datetime.now()
		dt_aware = time_str.strftime('%Y%m%d%H%M%S')

		la,lo = getLatLong()
		messageStr = 'M' + str(messageCount)
		time_r = getTime()

		#fileName = "IMG_" + str(TTL) + "_" + random.choice(type_list) + "_" + str(SOURCE) + "_defaultMcs_" + str(la) + "_" + str(lo) + "_" + time_r + "_1.jpg"	
		size = 	random.randint(x_range,y_range)
		print str(step_size) + " " + created + " " + str(messageStr) + " " + str(source) + " " + str(destination) + " " + str(size) + " " + str(la) + " " + str(lo) + " " + str(time_r) + " " + random.choice(type_list)
		messageCount += 1
		step_size += stepSizeCounter
		i += 1
	#genFile(fileName,size)
