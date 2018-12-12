import ftplib
import os, sys, time

sync_dir = './'
addr = 'localhost'
if len(sys.argv)>=3:
    addr = sys.argv[1]
    sync_dir = sys.argv[2]

ftp = ftplib.FTP('')
ftp.connect(addr,8021)
ftp.login()
# ftp.cwd('directory_name')
ftp.cwd('./')
ftp.retrlines('LIST')
ftp.retrlines('NLST')
print("===========")


def download(ftp):
    filematch = "*"
    for filename in ftp.nlst():
        print(filename)
        if os.path.exists(sync_dir + filename) == False:
            fhandle = open(os.path.join(sync_dir, filename), 'wb')
            print('Getting ' + filename)
            ftp.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        elif os.path.exists((sync_dir + filename)) == True:
            print('File ', filename, ' Already Exists, Skipping Download')

lc=0 
def downloadFiles(path,destination):
#path & destination are str of the form "/dir/folder/something/"
#path should be the abs path to the root FOLDER of the file tree to download
    try:
        ftp.cwd(path)
        #clone path to destination
        
        os.chdir(destination)
        os.mkdir(destination[0:len(destination)-1]+path)
        print(destination[0:len(destination)-1]+path+" built")
    except OSError:
        #folder already exists at destination
        pass
    except ftplib.error_perm:
        #invalid entry (ensure input form: "/dir/folder/something/")
        print("error: could not change to "+path)
        sys.exit("ending session")

    #list children:
    filelist=ftp.nlst()

    for file in filelist:
        try:
            #this will check if file is folder:
            ftp.cwd(path+file+"/")
            #if so, explore it:
            downloadFiles(path+file+"/",destination)
        except ftplib.error_perm:
            #not a folder with accessible content
            #download & return
            os.chdir(destination[0:len(destination)-1]+path)
            #possibly need a permission exception catch:
            ftp.retrbinary("RETR "+file, open(os.path.join(destination,file),"wb").write)
            print(file + " downloaded")
    return

while True:
    # download(ftp)
    downloadFiles('./',sync_dir)
    print("Waint 30sec")
    time.sleep(30)