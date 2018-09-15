import os
import sys
import json
import time
from influxdb import InfluxDBClient

base_dir = sys.argv[1]

counter= {}

myclient = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', database='gis')

while (True):

	try:
		text=myclient.query('select count(text) from kml')
		text = list(text.get_points(measurement='kml'))
		counter['text']=text[0]['count']
	except:
		counter['text']=0

	try:
		image=len(os.listdir(os.path.join(base_dir,"SurakshitImages")))
		image_list = os.listdir(os.path.join(base_dir,"SurakshitImages"))
		counter['image']=image_list
	except:
		counter['image']=[]

	try:
		video=len(os.listdir(os.path.join(base_dir,"SurakshitVideos")))
		video_list = os.listdir(os.path.join(base_dir,"SurakshitVideos"))
		counter['video']=video_list
	except:
		counter['video']=[]

	try:
		audio=len(os.listdir(os.path.join(base_dir,"SurakshitAudio")))
		audio_list = os.listdir(os.path.join(base_dir,"SurakshitAudio"))
		counter['audio']=audio_list
	except:
		counter['audio']=[]

	try:
		pgp = len(os.listdir(os.path.join(base_dir,"pgpKey")))
		fileList = os.listdir(os.path.join(base_dir,"pgpKey"))
		contact_list=[]
		contact=0
		for j in range(len(fileList)):
			name=fileList[j][4:14]
			if(name.isdigit()):
				contact_list.append(name)
		counter['pgp']=contact_list
	except:
		counter['pgp']=[]
	try:
		mp = len(os.listdir(os.path.join(base_dir,"SurakshitMap")))
		map_list = os.listdir(os.path.join(base_dir,"SurakshitMap"))
		counter['sum']=map_list
	except:
		counter['sum']=[]





	#print(counter)
	counter_string=json.dumps(counter)
	file = open("counter.json",'w')

	file.write(counter_string)

	file.close()
	time.sleep(10)
