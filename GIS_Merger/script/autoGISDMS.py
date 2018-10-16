import sys,os
import datetime
import random
import exrex
import json
from shapely.geometry.polygon import LinearRing
from shapely.geometry import MultiPoint, Point
from math import sin,cos,pi
import numpy as np

# To output color text in terminal
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

if ((len(sys.argv) < 7)):
    print """\
This script creates file as per GIS format( accepted by DMS App )""" + color.BOLD + color.CYAN + """

Usage:  python autoGISDMS.py latitude longitude noOfFiles noOfDevices time_range dirName
""" + color.END + """
1. Filename will be randomly spread in the area near latitude and longitude
2. Give SOURCE the same as given in DMS app
3. time_range : Time difference from the current time
4. dirName : Directory at which you want to rename the files

VARIABLES
----------
1. Type Of GIS Shape (Point, LineString, Polygon)


EXTENSION OF FILE CREATED
--------------------------
1. .geojson
"""
    sys.exit(1)


lat = float(sys.argv[1])
lon = float(sys.argv[2])
noOfFiles = int(sys.argv[3])
noOfDevices = int(sys.argv[4])
TTL = 50
time_range = int(sys.argv[5])
dirName = sys.argv[6]
if not os.path.exists(dirName):
    os.makedirs(dirName)
type_list = ["Victim","Shelter","Food","Health"]
shape_list = ["Point", "LineString", "Polygon"]
source_list = []

def getLatLong():
	"""
	Spread messages in area of lat-long (More spreadVal more spreaded area)
	"""
	val = random.randint(0,100)
	if val < 20:
		spreadVal = 2000

	else:
		spreadVal = 1500

	v = random.randint(0,3)
	if v == 0:
		la = float(lat - float(random.randint(0,spreadVal))/1000000.0)
		lo = float(lon + float(random.randint(0,spreadVal))/1000000.0)
	elif v==1:
		la = float(lat + float(random.randint(0,spreadVal))/1000000.0)
		lo = float(lon - float(random.randint(0,spreadVal))/1000000.0)
	elif v==2:
		la = float(lat + float(random.randint(0,spreadVal))/1000000.0)
		lo = float(lon + float(random.randint(0,spreadVal))/1000000.0)
	elif v==3:
		la = float(lat - float(random.randint(0,spreadVal))/1000000.0)
		lo = float(lon - float(random.randint(0,spreadVal))/1000000.0)
	
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
    random_second = random.randrange(abs(int_delta))
    return start + datetime.timedelta(seconds=random_second)

def getTime():
	d2 = datetime.datetime.now()
	change = random.choice([True, False])
	if change:
		d1 = d2 + datetime.timedelta(hours=time_range)
	else:	
		d1 = d2 - datetime.timedelta(hours=time_range)	
	return random_date(d1, d2).strftime('%Y%m%d%H%M%S')

def computeSourceList():
	"""
	Create Indian Telephonic Numbers for total no. of devices
	"""
	count = 0
	while count < noOfDevices:
		# Generate Indian Phone Numbers
		source_list.append(exrex.getone('[7-9]{2}\d{8}').encode('ascii', 'ignore'))
		count = count + 1

def generatePoint():
	return getLatLong()

# Create Indian Phone Numbers List based on total noOfDevices entered
computeSourceList()

# Generate GIS messages 
for i in range(noOfFiles):

	time_r = getTime()

	# Create geojson messages
	geoMessage = {}
	geoMessage["type"] = "FeatureCollection"
	geoMessage["features"] = []
	geoMessage["features"].append("")
	geoMessage["features"][0] = {}

	geoMessage["features"][0]["type"] = "Feature"

	geoMessage["features"][0]["properties"] = {}
	geoMessage["features"][0]["properties"]["PO"] = {}
	geoMessage["features"][0]["properties"]["PR"] = {}
	geoMessage["features"][0]["properties"]["Source"] = random.choice(source_list) 
	geoMessage["features"][0]["properties"]["PO"]["timestamp"] = getTime()
	geoMessage["features"][0]["properties"]["PR"]["timestamp"] = getTime()
	geoMessage["features"][0]["properties"]["PO"]["coordinate"] = map(float, getLatLong())
	geoMessage["features"][0]["properties"]["PR"]["coordinate"] = map(float, getLatLong())
	geoMessage["features"][0]["geometry"] = {}

	# Generate Random Shapes (1 - Point, 2 - LineString, 3 - Polygon)
	shape_rand = "Polygon"
	geoMessage["features"][0]["geometry"]["type"] = shape_rand

	if shape_rand == "Point":
		# Create Point coordinates
		pointVal = generatePoint()	
		geoMessage["features"][0]["geometry"]["coordinates"] = map(float, pointVal)
	elif shape_rand == "LineString":
		# Create LineString coordinates
		geoMessage["features"][0]["geometry"]["coordinates"] = []
		pointVal1 = generatePoint()
		pointVal2 = generatePoint()	
		geoMessage["features"][0]["geometry"]["coordinates"].append(map(float, pointVal1))
		geoMessage["features"][0]["geometry"]["coordinates"].append(map(float, pointVal2))		
	else:
		countNoOfPointsInPolygon = random.randint(4,8)
		geoMessage["features"][0]["geometry"]["coordinates"] = []
		geoMessage["features"][0]["geometry"]["coordinates"].append("")
		geoMessage["features"][0]["geometry"]["coordinates"][0] = []
		pointVal1 = generatePoint()
		
		x = [float(pointVal1[0])];
		y = [float(pointVal1[1])];
		r = 0;
		angle = 0
		for i in range(1,countNoOfPointsInPolygon):
		    angle += 0.8 + random.uniform(0, 1) * 0.8
		    if angle > 2 * pi:
		    	break   #stop before it becomes convex
		    r = (0.1 + random.uniform(0, 1) * 0.009+random.uniform(0, 1)*0.1)
		    x.append(x[i - 1] + r * cos(angle));
		    y.append(y[i - 1] + r * sin(angle));
		x.append(x[0])
		y.append(y[0])
		combined = np.vstack((x, y)).T.tolist()
		geoMessage["features"][0]["geometry"]["coordinates"][0] = list(combined)
		
		# for items in range(0,countNoOfPointsInPolygon-1):
		# 	pointVal = generatePoint()
		# 	arr.append(pointVal)
		# 	geoMessage["features"][0]["geometry"]["coordinates"][0].append(map(float, pointVal))
		#geoMessage["features"][0]["geometry"]["coordinates"][0].append(map(float, pointVal1))
		
		
	d = json.dumps(geoMessage)
    
	filename="GIS_50_Gis_" + str(geoMessage["features"][0]["properties"]["Source"])+ "_defaultMCS_"+str(geoMessage["features"][0]["properties"]["PR"]["coordinate"][0])+"_"+str(geoMessage["features"][0]["properties"]["PR"]["coordinate"][1])+"_"+str(geoMessage["features"][0]["properties"]["PR"]["timestamp"])+"_"+str(files)+'.txt'
	with open(os.path.join(dirName, filename), 'wb') as tempfile:
		tempfile.write(d)
	tempfile.close()
