import sys,os
import datetime
import random
lat = float(sys.argv[1])
lon = float(sys.argv[2])
noOfFiles = int(sys.argv[3])

x_range = float(sys.argv[4])
y_range = float(sys.argv[5])

TTL = 50
SOURCE = sys.argv[6]
time_range = int(sys.argv[7])

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


for i in range(noOfFiles):
	time_str = datetime.datetime.now()
	dt_aware = time_str.strftime('%Y%m%d%H%M%S')
	#print dt_aware

	la,lo = getLatLong()
	time_r = getTime()
	fileName = "IMG_" + str(TTL) + "_" + random.choice(type_list) + "_" + str(SOURCE) + "_defaultMcs_" + str(la) + "_" + str(lo) + "_" + time_r + "_1.jpg"	
	size = 	random.randint(x_range,y_range)
	genFile(fileName,size)
