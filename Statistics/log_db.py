import csv
import datetime
import sys
import json
from dateutil import parser



file_size={}
peer_data={}
peer_user={}
res_peer = {}  # stores only completed and allowed file formats
storage={}
peer_file_count = {}
peer_file_size = {}
visit ={}

file_formats = [".jpeg",".jpg",".3pg",".mp4",".mkv",".png",".wav",".kml"]

date_file = sys.argv[2]
filename=sys.argv[1]

cur_check=0
def time_parse(datestring):
	return datetime.datetime.strptime(datestring,"%Y.%m.%d.%H.%M.%S")+datetime.timedelta(days=1)


def date_parser(datestring):
	# dt = parser.parse("Aug 28 1999 12:45AM")
	dt = parser.parse(datestring)
	print (dt)
	return str(dt)



def check_time_range(start,end,t):
	if start <= t < end:
		return True
	else:
		return False

def greater(end,t):
	if(t<=end):
	  return False
	else:
		return True


def statistics(start,end):
	global cur_check
	global file_size
	global peer_data
	global peer_user
	global res_peer
	global storage
	global peer_file_count
	global peer_file_size
	global visit
	global file_formats
	print ("cur_check= ",cur_check)
	logfile=open(filename,'r')
	logread=csv.reader(logfile)
	start = time_parse(start)
	end = time_parse(end)
	cc=0
	for row in logread:
		if cc<cur_check:
			cc +=1
			continue
		cc +=1
		if row[1].endswith('PEER_DISCOVERED'):
				peer_user[row[3]]=row[2]
		if not row[1].endswith('_FILE_DOWNLOAD'):
			continue
		if row[1]==' START_FILE_DOWNLOAD':
			if check_time_range(start,end, time_parse(row[0])):
				user = peer_user.get(row[6])
				if user in peer_data:
					peer_data[user].append(row[3])
				else:
					peer_data.update({user:[row[3]]})

				file_size.update({row[3]:[row[4],row[5]]})

		if row[1]==' STOP_FILE_DOWNLOAD':
			if check_time_range(start,end, time_parse(row[0])):
				file_size.update({row[3]:[row[4],row[5]]})#update sixe again, bad log
		if(greater(end,time_parse(row[0]))):
			cur_check=cc
			break



	for peer,flie_list in peer_data.items():
		total = 0
		# print("Peer: %s" %peer)
		for f in flie_list:
			if f in file_size:
				s = file_size.get(f)
				if float(s[0].strip()) >= float(s[1].strip()):
					if f.endswith(tuple(file_formats)):
						if peer in res_peer:
							res_peer[peer].append([f,s[1]])
						else:
							res_peer.update({peer:[f,s[1]]})

					# print("			: file {} : downloaded completely.".format(f))
				else:
					# print("			: file {} : downloaded partialy.".format(f))
					pass


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
				visit[f[0]]=1
			if f[0].endswith(".jpeg"): 
				file_count["image"] += 1
				file_storage["image"] +=float(f[1])
			if f[0].endswith(".png"):
				file_count["map"] +=1
				file_storage["map"] +=float(f[1])
			if f[0].endswith(".mp4"):
				file_count["video"] += 1
				file_storage["video"] +=float(f[1])
			if f[0].endswith(".3pg"):
				file_count["audio"] += 1
				file_storage["audio"] +=float(f[1])

			peer_file_count.update({peer : [file_count,file_storage]})
		# print(file_count)
	file = open("stat.csv",'a')
	file_content = json.dumps(peer_file_count)
	file.write(file_content)
	file.write("\n"+"\n"+"*******************************************************************"+"\n"+"\n"+"\n")
	file.close()
	print(peer_file_count)

	logfile.close()


# options={'-h':print(help_doc),'-p':peer_phrase(),'-d':data_phrase()}

# start = time_parse(sys.argv[2])
# end = time_parse(sys.argv[3])



def readDate(filename):
	text=open(filename,'r')
	content = text.read().splitlines()
	r_no=0
	for row in content:
		if r_no==0:
			r_no +=	1
			continue
		start = content[r_no-1]
		end = content [r_no]
		r_no +=1
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
		print (start_time,end_time)
		statistics(start_time,end_time)



readDate(date_file)






