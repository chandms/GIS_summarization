import csv
import datetime
import sys
import json
from dateutil import parser
import os
import codecs

check={}
file_size={}
peer_data={}
res_peer = {}  # stores only completed and allowed file formats
storage={}
peer_file_count = {}
peer_file_size = {}
visit ={}
total_video = 0
total_audio = 0
total_image = 0
total_map =0
file_formats = [".jpeg",".jpg",".3pg",".mp4",".mkv",".png",".wav",".kml"]

date_file = sys.argv[1]


def time_parse(datestring):
	return datetime.datetime.strptime(datestring,"%Y.%m.%d.%H.%M.%S")+datetime.timedelta(days=1)


def date_parser(datestring):
	# dt = parser.parse("Aug 28 1999 12:45AM")
	dt = parser.parse(datestring)
	print (dt)
	return str(dt)



def check_time_range(start,end,t):
	if start <= t <= end:
		return True
	else:
		return False

def greater(end,t):
	if(t<=end):
	  return False
	else:
		return True


def statistics(file_name,start,end):
	pr_start=start
	pr_end=end
	global file_size
	global peer_data
	global res_peer
	global storage
	global peer_file_count
	global peer_file_size
	global visit
	global file_formats
	global total_image
	global total_video
	global total_audio
	global total_map
	global check
	print("file_name = ",file_name)
	logfile=open(file_name,'rb')
	logread = csv.reader((line.replace('\0','') for line in logfile), delimiter=",")
	if(start!="filler"):
		start = time_parse(start)
	end = time_parse(end)
	print("CM",start,end)
	cc=0
	ct=0
	if logread is not None:
		for row in logread:
			if start=="filler" and ct==0:
				start=row[0]
				start=time_parse(start)
				ct +=1
				print("pupul ",start,end)
			if not row[1].endswith('_FILE_DOWNLOAD'):
				continue
			if row[1]==' START_FILE_DOWNLOAD':
				if row[3].endswith(tuple(file_formats)):
					if check_time_range(start,end, time_parse(row[0])):
						ll=row[3].split('_')
						y=0
						while y<len(ll[1]):
							if(ll[1][y].isdigit()):
								break
							y +=1
						ll[1]=ll[1][y:]
						if ll[1] in peer_data:
							peer_data[ll[1]].append(row[3])
						else:
							peer_data.update({ll[1]:[row[3]]})

						file_size.update({row[3]:[row[4],row[5]]})

			if row[1]==' STOP_FILE_DOWNLOAD':
				if check_time_range(start,end, time_parse(row[0])):
					file_size.update({row[3]:[row[4],row[5]]})#update sixe again, bad log
			# if(greater(end,time_parse(row[0]))):
			# 	break



		# for peer,flie_list in peer_data.items():
		# 	total = 0
		# 	# print("Peer: %s" %peer)
		# 	for f in flie_list:
		# 		if f in file_size:
		# 			s = file_size.get(f)
		# 			if float(s[0].strip()) >= float(s[1].strip()):
		# 				if f.endswith(tuple(file_formats)):
		# 					if peer in res_peer:
		# 						res_peer[peer].append([f,s[1]])
		# 					else:
		# 						res_peer.update({peer:[f,s[1]]})

		# 				# print("			: file {} : downloaded completely.".format(f))
		# 			else:
		# 				# print("			: file {} : downloaded partialy.".format(f))
		# 				pass


		for peer,flie_list in peer_data.items():
			total = 0
			# print("Peer: %s" %peer)
			for f in flie_list:
				if f=='1a5b38d26c6829a459875f1dab80abfd_v9674209814_volunteer_50_44ba374447c33b05.jpeg':
					print "cooleo"
				if f in file_size:
					s = file_size.get(f)
					# if float(s[0].strip()) >= float(s[1].strip()):
					
					if f.endswith(tuple(file_formats)):
						if('9674209814' in f and ".jpeg" in f):
							check[f]=1
						if peer in res_peer:
							res_peer[peer].append([f,s[0]])
						else:
							res_peer.update({peer:[f,s[0]]})





		for peer, files in res_peer.items():
			# print("Peer {} : Total Files of specified formats: {}".format(peer, len(files)))\
			file_count={}
			file_storage={}
			if peer in peer_file_count:
				xs = peer_file_count[peer]
				file_count =xs[0]
				file_storage = xs[1]
			else:
				file_count ={ "image": 0, "video": 0, "audio": 0 ,"map":0}
				file_storage = {"image": 0.0, "video": 0.0, "audio": 0.0 ,"map":0.0}
			for f in files:
				if f[0] in visit:
					continue
				else:
					if '9674209814' in f[0]:
						print f[0],"heyya"
					visit[f[0]]=1
					if f[0].endswith(".jpeg"): 
						file_count["image"] += 1
						file_storage["image"] +=float(f[1])
						total_image +=1
					if f[0].endswith(".png"):
						file_count["map"] +=1
						file_storage["map"] +=float(f[1])
						total_map +=1
					if f[0].endswith(".mp4"):
						file_count["video"] += 1
						file_storage["video"] +=float(f[1])
						total_video +=1
					if f[0].endswith(".3pg"):
						file_count["audio"] += 1
						file_storage["audio"] +=float(f[1])
						total_audio +=1

				peer_file_count.update({peer : [file_count,file_storage]})
			# print(file_count)
		

		
		
		tot_list = []
		if(pr_start=="filler"):
			pr_start="initiation"
		tot_list.append(pr_start+"-"+pr_end)
		tot_list.append(str(total_image))
		tot_list.append(str(total_video))
		tot_list.append(str(total_audio))
		tot_list.append(str(total_map))
		with open('overall.csv','a') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(tot_list)
			csv_file.close()
		if "null" in peer_file_count:
			del peer_file_count["null"]
		with open('stat.csv','a') as csv_file2:
			writer=csv.writer(csv_file2)
			for key,value in peer_file_count.iteritems():
				ins_tab=[]
				ins_tab.append(pr_start+"-"+pr_end)
				ins_tab.append(key)
				l1= peer_file_count[key][0]
				l2=peer_file_count[key][1]
				ins_tab.append(str(l1["image"]))
				ins_tab.append(str(l1["video"]))
				ins_tab.append(str(l1["audio"]))
				ins_tab.append(str(l1["map"]))
				ins_tab.append(str(l2["image"]))
				ins_tab.append(str(l2["video"]))
				ins_tab.append(str(l2["audio"]))
				ins_tab.append(str(l2["map"]))
				writer.writerow(ins_tab)
			csv_file2.close()

		print(peer_file_count)

	logfile.close()


# options={'-h':print(help_doc),'-p':peer_phrase(),'-d':data_phrase()}

# start = time_parse(sys.argv[2])
# end = time_parse(sys.argv[3])



def readDate(date_file,file_name):
	text=open(date_file,'r')
	content = text.read().splitlines()
	r_no=0
	for row in content:
		start_time=""
		end_time=""
		if r_no==0:
			start="filler"
			end = content[r_no]
			en = end.split('%')
			end_time = date_parser(en[0])
			en = end_time.split(' ')
			temp=en[1].split('+')
			en[1]=temp[0]
			start_time="filler"
			end_time=""

			temp1 = en[0].split('-')
			for c in range(len(temp1)):
				end_time = end_time +temp1[c]+"."
			temp1=en[1].split(':')
			for c in range(len(temp1)):
				end_time = end_time +temp1[c]+"."
			le=len(end_time)
			end_time = end_time[0:le-1]
		else:
			start = content[r_no-1]
			end = content [r_no]
			st = start.split('%')
			start_time = date_parser(st[0])
			en = end.split('%')
			end_time = date_parser(en[0])
			st = start_time.split(' ')
			en = end_time.split(' ')
			temp = st[1].split('+')
			st[1]=temp[0]
			temp=en[1].split('+')
			en[1]=temp[0]
			temp1= st[0].split('-')
			start_time=""
			end_time=""
			for c in range(len(temp1)):
				start_time=start_time+temp1[c]+"."
			temp1 = st[1].split(":")
			for c in range(len(temp1)):
				start_time=start_time+temp1[c]+"."
			ls= len(start_time)
			start_time = start_time[0:ls-1]

			temp1 = en[0].split('-')
			for c in range(len(temp1)):
				end_time = end_time +temp1[c]+"."
			temp1=en[1].split(':')
			for c in range(len(temp1)):
				end_time = end_time +temp1[c]+"."
			le=len(end_time)
			end_time = end_time[0:le-1]
		r_no +=1
		print (start_time,end_time)
		statistics(file_name,start_time,end_time)


f_list = os.listdir("./")
f_list.sort()
tot_col=['timeStamp','image','video','audio','map']
top_col=["timeStamp","Node_id","image_count","video_count","audio_count","map_count","image_volume","video_volume","audio_volume","map_volume"]
with open('overall.csv','a') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(tot_col)
	csv_file.close()
with open('stat.csv','a') as csv_file2:
	writer = csv.writer(csv_file2)
	writer.writerow(top_col)
	csv_file2.close()
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
			readDate(date_file,"./"+cur_file)

for key,vk in peer_data.iteritems():
	print(key)

for key,vk in check.iteritems():
	print(key)






