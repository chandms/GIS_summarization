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
file_count =0

def time_parse(datestring):
	return datetime.datetime.strptime(datestring,"%Y.%m.%d.%H.%M.%S")+datetime.timedelta(days=1)

file_formats = [".jpeg",".jpg",".3pg",".mp4",".mkv",".png",".wav",".kml",".txt",".bgp"]

files_stored={}
x1_axis=[]
y1_axis=[]
x2_axis=[]
y2_axis=[]
x3_axis=[]
y3_axis=[]

count_dict = defaultdict(list)
file_dict = defaultdict(list)
type_dict= defaultdict(list)
counter=0
existance ={}
time_start=datetime.datetime.now()
time_end=datetime.datetime.now()

def statistics(file_name,realfile):
	peer_user={}
	global count_dict
	global current_volume
	global total_volume
	global x1_axis
	global x2_axis
	global y1_axis
	global y2_axis
	global time_start
	global time_end
	global counter
	global file_count
	global file_dict
	print("file_name = ",file_name)
	
	
	logreal = open(realfile,'r')
	realread = csv.reader(logreal)

	time_list=[]
	value=[]
	if realread is not None:
		for ro in realread:
			time_list.append(time_parse(ro[0]))
			fn=ro[1].split('_')
			value.append(fn[0])
	print(time_list)
	print(value)
	cc=0
	fi=0
	li=1
	ind =0
	while ind in range(len(time_list)):
		fi=ind
		ind +=1
		while ind <len(time_list) and value[ind]==' START':
			ind +=1
		while ind <len(time_list) and value[ind]==' STOP':
			ind +=1
		ind = ind -1
		li=ind
		ind +=1
		if (li<len(time_list)):
			print(fi,li,ind)
			logfile=open(file_name,'r')
			logread = csv.reader(logfile)
			if logread is not None:
				for row in logread:
					if (time_parse(row[0])<time_list[li]):
						if row[1]==" PEER_DISCOVERED":
							counter +=1
						elif(row[1]==" PEER_LOST"):
							counter =counter -1

						elif row[1]==' START_FILE_DOWNLOAD' and time_parse(row[0])>=time_list[fi]:
							if row[3].endswith(tuple(file_formats)):
								name_of_file = row[3]
								if(name_of_file in files_stored):
									current_volume +=float(row[4])-files_stored[name_of_file]
									total_volume+=float(row[4])-files_stored[name_of_file]
									files_stored[name_of_file]=float(row[4])
									if(files_stored[name_of_file]>0):
										file_count +=1
									if name_of_file not in existance:
										tag=name_of_file.split('.')
										print("tag = ",name_of_file)
										type_dict[tag[1]].append(name_of_file)
										existance[name_of_file]=1

								else:
									current_volume +=float(row[4])
									total_volume +=float(row[4])
									files_stored[name_of_file]=float(row[4])
									if(files_stored[name_of_file]>0):
										file_count +=1
									if name_of_file not in existance:
										tag=name_of_file.split('.')
										print("tag = ",name_of_file)
										type_dict[tag[1]].append(name_of_file)
										existance[name_of_file]=1
										




						elif row[1]==' STOP_FILE_DOWNLOAD' and time_parse(row[0])>=time_list[fi]:
							if row[3].endswith(tuple(file_formats)):
								name_of_file = row[3]
								if(name_of_file in files_stored):
									current_volume +=float(row[4])-files_stored[name_of_file]
									total_volume+=float(row[4])-files_stored[name_of_file]
									files_stored[name_of_file]=float(row[4])
									if(files_stored[name_of_file]>0):
										file_count +=1
									if name_of_file not in existance:
										tag=name_of_file.split('.')
										print("tag = ",name_of_file)
										type_dict[tag[1]].append(name_of_file)
										existance[name_of_file]=1
								else:
									current_volume +=float(row[4])
									total_volume +=float(row[4])
									files_stored[name_of_file]=float(row[4])
									if(files_stored[name_of_file]>0):
										file_count +=1
									if name_of_file not in existance:
										tag=name_of_file.split('.')
										print("tag = ",name_of_file)
										type_dict[tag[1]].append(name_of_file)
										existance[name_of_file]=1
					elif(time_parse(row[0])>=time_list[li]):
						time_diff = time_list[li]-time_list[fi]
						time_diff_sec = time_diff.total_seconds() 
						if time_diff_sec !=0:

							data_rate = current_volume/time_diff_sec
							count_rate = file_count/time_diff_sec
							count_dict[counter].append(data_rate)
							file_dict[counter].append(count_rate)
							with open('Data_flow.text','a') as res_file:
								timing = time_parse(row[0])
								res_file.write(str(time_diff_sec)+" "+str(data_rate)+" "+str(counter)+"\n")
								res_file.close()
							print(time_diff_sec,data_rate,counter)

							y3_axis.append(total_volume)
							df=time_parse(row[0])
							print(df)
							x3_axis.append(df)
						current_volume=0
						counter=0
						file_count=0
						logfile.close()
						break
			




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
		fg=name.split('_')
		if(ns[0]=="psyncLog" and len(fg)==1):
			statistics(cur_file,'final_file.csv')

if 0 in file_dict:
	print("it's here though")
else:
	file_dict[0].append(0.0)
if 0 in count_dict:
	print("it's here")
else:
	count_dict[0].append(0.0)
std_ar=[]
for key,vt in count_dict.items():
	sum=0
	sp=0
	for k in range(len(count_dict[key])):
		sum=sum+count_dict[key][k]
	sum=sum/len(count_dict[key])
	for g in range(len(file_dict[key])):
		sp = sp+file_dict[key][g]
	sp=sp/len(file_dict[key])
	cur_std = np.std(count_dict[key])
	std_ar.append(cur_std)
	x2_axis.append(key)
	y2_axis.append(sum)
	x1_axis.append(key)
	y1_axis.append(sp)

index = np.arange(len(x2_axis))
# (_, caps, _) = plt.errorbar(x2_axis, y2_axis, std_ar, capsize=10, elinewidth=10,markeredgewidth=2,marker='^')
#print(std_ar)
print(y2_axis)
plt.bar(x2_axis,y2_axis)
# plt.errorbar(x2_axis, y2_axis,std_ar,elinewidth=25,markeredgewidth=2,marker='^')
# plt.bar(x2_axis,y2_axis)
# for cap in caps:
#     cap.set_color('red')
#     cap.set_markeredgewidth(10)
plt.xlabel('node_count', fontsize=15)
plt.ylabel('data_rate', fontsize=15)
plt.xticks(index, x2_axis, fontsize=15, rotation=30)
plt.title('data rate vs connected_node_count')
plt.show()

index = np.arange(len(x1_axis))
print(y1_axis)
plt.bar(x1_axis,y1_axis)
# plt.errorbar(x2_axis, y2_axis,std_ar,elinewidth=25,markeredgewidth=2,marker='^')
# plt.bar(x2_axis,y2_axis)
# for cap in caps:
#     cap.set_color('red')
#     cap.set_markeredgewidth(10)
plt.xlabel('node_count', fontsize=15)
plt.ylabel('file_count_rate', fontsize=15)
plt.xticks(index, x1_axis, fontsize=15, rotation=30)
plt.title('file_count_rate vs connected_node_count')
plt.show()

plt.plot(x3_axis,y3_axis)
plt.xlabel('time',fontsize=15)
plt.ylabel('total_volume',fontsize=15)
plt.title('total_volume vs time')
plt.show()

x_axis=['video','audio','image','map','txt']
y_axis=[0,0,0,0,0]
for key,vt in type_dict.items():
	if(key=='txt'):
		y_axis[4]+=len(type_dict[key])
	elif(key=='mp4'):
		y_axis[0] +=len(type_dict[key])
	elif(key=='3gp'):
		y_axis[1] +=len(type_dict[key])
	elif(key=='jpeg'):
		y_axis[2] +=len(type_dict[key])
	elif(key=='png'):
		y_axis[3] +=len(type_dict[key])


print(x_axis)
print(y_axis)

index = np.arange(len(x_axis))
print(index)
plt.bar(index,y_axis,align='center')
plt.xlabel('type',fontsize=15)
plt.ylabel('count_of_type',fontsize=15)
plt.xticks(index, x_axis)
plt.title('count vs type of file')
plt.show()








