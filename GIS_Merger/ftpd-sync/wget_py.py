import subprocess
import sys
import os
import time

sync_dir = './'
addr = 'localhost'
if len(sys.argv)>=3:
    addr = sys.argv[1]
    sync_dir = sys.argv[2]

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), sync_dir)
print(dir_path)
# wget -nc -np -nH -r 'ftp://user:12345@localhost:8021/'
wget_cmd = "wget -nc -nv -np -nH -r ftp://user:12345@"+addr+":8021/"

while True:
    try:
        subprocess.run(wget_cmd, shell=True,cwd=dir_path)
        print("Wait 60sec...")
        time.sleep(60)
    except Exception as e:
        print("=========== EXCEPTION ===========")
        print(e)
        sys.exit(1)
