import subprocess
import time
import os

#In download sense
src = "/home/pi/ftpd-sync/work/"
src_mod = "/files/"
dst = "/home/pi/ftpd-sync/work/"

rsync_down = "rsync -avzh rsync://192.168.0.5:8585"+src_mod+" "+dst
rsync_up = "rsync -avzh "+dst+" rsync://192.168.0.5:8585"+src_mod

#first download
def download():
    p = subprocess.run(rsync_down, shell=True)
    return p

def upload():
    p = subprocess.run(rsync_up, shell=True)
    return p

while True:
    d = download()
    time.sleep(30)
    u = upload()
    time.sleep(30)
