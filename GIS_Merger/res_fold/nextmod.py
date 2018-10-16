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

def takerowzero(lm):
    return time_parse(lm[0])


def time_parse(datestring):
	return datetime.datetime.strptime(datestring,"%Y.%m.%d.%H.%M.%S")+datetime.timedelta(days=1)

row_list=[]
def files_parser(filename):
	global row_list
	logfile=open(filename,'r')
	logread = csv.reader(logfile)
	if logread is not None:
		for row in logread:
			row_list.append(row)

def sorted_storing():
	for r in range(len(row_list)):
		if(row_list[r] is None):
			del row_list[r]

	row_list.sort(key=takerowzero)
	for k in range(len(row_list)):
		with open('final_file.csv','a') as csvread:
			writer = csv.writer(csvread)
			writer.writerow(row_list[k])


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
		ns=name.split('-')
		if(ns[0]=="psyncLog"):
			fg=name.split('_')
			if(len(fg)==2):
				files_parser(cur_file)
sorted_storing()

