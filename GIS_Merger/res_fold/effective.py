import csv
import datetime
import sys
import json
from dateutil import parser
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import statistics



current_volume =0
total_volume =0

def time_parse(datestring):
	return datetime.datetime.strptime(datestring,"%Y.%m.%d.%H.%M.%S")+datetime.timedelta(days=1)

file_formats = [".jpeg",".jpg",".3pg",".mp4",".mkv",".png",".wav",".kml",".txt",".bgp"]

files_stored={}
x1_axis=[]
y1_axis=[]
x2_axis=[]
y2_axis=[]

count_dict = defaultdict(list)

counter=0

time_start=datetime.datetime.now()
time_end=datetime.datetime.now()


peer_ids={}

def each_node(file_name):
	logfile=open(file_name,'r')
	logread = csv.reader(logfile)
	if logread is not None:
		for row in logread:
			if row[1]==' PEER_DISCOVERED':
				peer_ids[row[2]]=1
	logfile.close()
	peer_user={}
	for peer,val in peer_ids.items():
		logfile = open(file_name,'r')
		logread = csv.reader(logfile)
		detect = 0 
		download = 0 
		start_string=""
		special_string =""
		if logread is not None:
		 	for row in logread:
		 		if detect ==0 and row[1]==' PEER_DISCOVERED' and peer==row[2]:
		 			peer_user[row[3]]=row[2]
		 			print(peer,peer_user[row[3]],row[3])
		 			# print("hi1")
		 			detect = 1
		 		elif detect ==1 and download == 0:
		 			# print("hi2")
		 			if row[1]==' START_FILE_DOWNLOAD' and row[6] in peer_user and peer_user[row[6]]==peer:
		 				start_string=row
		 				download=1

		 			elif row[1]==' START_FILE_DOWNLOAD' and peer==row[6]:
		 				start_string=row
		 				download=1
		 		elif detect ==1 and download == 1 and (row[1]==' START_FILE_DOWNLOAD' or row[1]==' STOP_FILE_DOWNLOAD') and ((row[6] in peer_user and peer_user[row[6]]==peer) or peer==row[6]):
		 			# print("hi3")
		 			if row[1]==' START_FILE_DOWNLOAD':
		 				special_string = row
		 			if row[1]==' STOP_FILE_DOWNLOAD':
		 				special_string = row
		 		elif row[1]==' PEER_LOST' and ((row[3] in peer_user and peer_user[row[3]]==peer) or peer==row[3]):
		 			# print("hi4")
		 			print("gotcha")
		 			with open(os.path.basename(file_name)+"_"+peer+".csv", 'a') as writeFile:
		 				writer = csv.writer(writeFile)
			 			writer.writerow(start_string)
			 			writer.writerow(special_string)
			 			detect =0
			 			download =0
		logfile.close()






f_list = os.listdir("./")
f_list.sort()


for cur_file in f_list:
	ll=0
	try:
		n_file = open("./"+cur_file,'r')
	except:
		ll +=1
	if ll==0:
		name=os.path.basename(n_file.name)
		fg= name.split('_')
		ns=name.split('-')
		if(ns[0]=="psyncLog"):
			print(cur_file)
			each_node(cur_file)





