import os
import sys
import json
import time
from influxdb import InfluxDBClient
from collections import defaultdict

base_dir = sys.argv[1]

counter= {}
information=defaultdict(list)

myclient = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', database='gis')

while (True):
	try:
		pgp = len(os.listdir(os.path.join(base_dir,"pgpKey")))
		fileList = os.listdir(os.path.join(base_dir,"pgpKey"))
		contact_list=[]
		contact=0
		for j in range(len(fileList)):
			name=fileList[j][4:14]
			if(name.isdigit()):
				contact_list.append(name)
				information[name]=[]
				information[name].append(0)
				information[name].append(0)
				information[name].append(0)
				information[name].append(0)
		counter['pgp']=contact_list
	except:
		counter['pgp']=[]

	try:
		text=myclient.query('select count(text) from kml')
		text = list(text.get_points(measurement='kml'))
		counter['text']=text[0]['count']
	except:
		counter['text']=0

	try:
		image=len(os.listdir(os.path.join(base_dir,"SurakshitImages")))
		image_list = os.listdir(os.path.join(base_dir,"SurakshitImages"))
		for k in range(len(image_list)):
			name = image_list[k].split('_')
			fg=0
			if(name[1].isdigit()):
				if(name[1] in contact_list):
					fg=fg+1
					information[name[1]][2]=information[name[1]][2]+1
			if(fg==0):
				y=0;
				while(y<range(len(name[1]))):
					if(name[1][y].isdigit()):
						break
					y +=1
				name[1]=name[1][y:]
				if(name[1].isdigit()):
					if(name[1] in contact_list):
						information[name[1]][2]=information[name[1]][2]+1
		counter['image']=image
	except:
		counter['image']=0

	try:
		video=len(os.listdir(os.path.join(base_dir,"SurakshitVideos")))
		video_list = os.listdir(os.path.join(base_dir,"SurakshitVideos"))
		for k in range(len(video_list)):
			name = video_list[k].split('_')
			fg=0
			if(name[1].isdigit()):
				if(name[1] in contact_list):
					fg=fg+1
					information[name[1]][0]=information[name[1]][0]+1
			if(fg==0):
				y=0;
				while(y<range(len(name[1]))):
					if(name[1][y].isdigit()):
						break
					y +=1
				name[1]=name[1][y:]
				if(name[1].isdigit()):
					if(name[1] in contact_list):
						information[name[1]][0]=information[name[1]][0]+1
		counter['video']=video
	except:
		counter['video']=0

	try:
		audio=len(os.listdir(os.path.join(base_dir,"SurakshitAudio")))
		audio_list = os.listdir(os.path.join(base_dir,"SurakshitAudio"))
		for k in range(len(audio_list)):
			name = audio_list[k].split('_') 
			fg=0                         
			if(name[1].isdigit()):
				if(name[1] in contact_list):
					fg=fg+1
					information[name[1]][1]=information[name[1]][1]+1
			if(fg==0):
				y=0;
				while(y<range(len(name[1]))):
					if(name[1][y].isdigit()):
						break
					y +=1
				name[1]=name[1][y:]
				if(name[1].isdigit()):
					if(name[1] in contact_list):
						information[name[1]][1]=information[name[1]][1]+1
		counter['audio']=audio
	except:
		counter['audio']=0


	try:
		mp = len(os.listdir(os.path.join(base_dir,"SurakshitMap")))
		map_list = os.listdir(os.path.join(base_dir,"SurakshitMap"))
		for k in range(len(map_list)):
			name = map_list[k].split('_')
			fg=0
			if(name[1].isdigit()):
				if(name[1] in contact_list):
					fg=fg+1
					information[name[1]][3]=information[name[1]][3]+1
			if(fg==0):
				y=0;
				while(y<range(len(name[1]))):
					if(name[1][y].isdigit()):
						break
					y +=1
				name[1]=name[1][y:]
				if(name[1].isdigit()):
					if(name[1] in contact_list):
						information[name[1]][3]=information[name[1]][3]+1
		counter['sum']=mp
	except:
		counter['sum']=0





	#print(counter)
	counter_string=json.dumps(counter)
	info = json.dumps(information)
	file = open("./fold/counter.json",'w')
	nfile = open("./fold/personified.json",'w')

	file.write(counter_string)
	nfile.write(info)

	file.close()
	nfile.close()
	time.sleep(10)
