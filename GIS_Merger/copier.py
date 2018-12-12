import numpy as np
import os.path
import glob
import os
import shutil
import ntpath
import time

lastvalue=-1


cv =0
for File in os.listdir('/home/pi/lr_test2/fold/'):
	if File.endswith("date.txt"):
		cv =1
		# x=ntpath.basename(File)
		x = File
	if File.endswith('merged.txt'):
		y = File
	if File.endswith('merge_time.conf'):
		z = File
	if File.endswith('counter.json'):
		w = File
	if File.endswith('personified.json'):
		v = File	



while(True):
	if cv==1:
		print("Copying started")
		f=open(x,"r")
		readval=""
		for xx in f:
			readval=xx
		f.close()
		val=readval.split('%')
		val=int(val[1])
		print(val,lastvalue)
		if val>lastvalue:
			lastvalue=val
			#shutil.rmtree('/home/pi/ftpd-sync/work/')
			#os.makedirs('/home/pi/ftpd-sync/work/')
			print ("lastvalue ", lastvalue)
			print ("copy ",x)
			shutil.copy2(x,'/home/pi/ftpd-sync/work/'+x)
			print ("copy ",y)
			shutil.copy2(y,'/home/pi/ftpd-sync/work/'+y)
			print ("copy ",z)
			shutil.copy2(z,'/home/pi/ftpd-sync/work/'+z)
			print ("copy ",w)
			shutil.copy2(w,'/home/pi/ftpd-sync/work/'+w)
			print ("copy ",v)
			shutil.copy2(v,'/home/pi/ftpd-sync/work/'+v)
		time.sleep(3)
