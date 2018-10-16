from collections import defaultdict


merge_file = open("obtained.txt",'w')
merge_file.write("")
merge_file.close()

with open("merged.txt",'r') as file:
    for line in file:
        arr = line.split('%')
        if(arr[2]=='cluster'):
            extra = arr[5]
            list_of_extra=extra.split('::')
            list_of_text=[]
            for tt in range(len(list_of_extra)):
                text = list_of_extra[tt]
                try:
                    if(text.endswith('.mp4') or text.endswith('.jpeg') or text.endswith('.3gp')):
                        continue
                    else:
                        #print (text)
                        list_of_text.append(text)
                except:
                    print("error")
            lat=[]
            long=[]
            cord = arr[0].split(',')
            for ind in range(len(cord)):
                ll = cord[ind].split(' ')
                lat.append(ll[0])
                long.append(ll[1])
            for ind in range(len(list_of_text)):
                if('\n' in list_of_text[ind]):
                    list_of_text[ind]=list_of_text[ind][:-1]
            if(len(list_of_text)!=0):
                merge_file=open('obtained.txt','a')
                merge_file.write(str(list_of_text)+":"+str(lat)+":"+str(long))
                merge_file.write("\n")
                merge_file.close()




