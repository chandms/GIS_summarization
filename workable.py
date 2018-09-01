import re
import time,os
from xml import dom
from influxdb import InfluxDBClient
import xml.etree.ElementTree as ET
from xml.dom.minidom import Node
from xml.dom import minidom
import collections
from influxdb import SeriesHelper
from lxml import etree
from io import StringIO
import sys
from xml.dom.minidom import parseString
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



fld=[]


myclient = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', database='gis')

class MySeriesHelper(SeriesHelper):
    # """Instantiate SeriesHelper to write points to the backend."""

    class Meta:
        # """Meta class stores time series helper configuration."""

        # The client should be an instance of InfluxDBClient.
        client = myclient

        # The series name must be a string. Add dependent fields/tags
        # in curly brackets.
        series_name = 'kml'

        # Defines all the fields in this time series.
        fields = fld

        # Defines all the tags for the series.
        tags = []

        # Defines the number of data points to store prior to writing
        # on the wire.
        bulk_size = 0

        autocommit= True


def traverse(root,myDict):
    global f
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                if(node.tagName=="Style"):
                    continue
                elif(node.tagName=='color' or node.tagName=='PolyStyle' or node.tagName=='LineStyle' or node.tagName=='width' ):
                    continue
                if(node.tagName=="Data"):
                    f="Data"+list(node.attributes.keys())[0]
                    for elem in node.attributes.values():
                        f=f+elem.firstChild.data
                    if(node.hasChildNodes()):
                        y = 0
                        for cn in node.childNodes:
                            if (y == 0):
                                myDict[f].append(cn.firstChild.nodeValue)
                            y = y + 1
                elif(node.tagName == 'value'):
                    continue
                else:
                    prev = node
                    for nn in node.childNodes:
                        if (nn.nodeType == Node.TEXT_NODE):
                            myDict[prev.tagName].append(nn.wholeText)
                            break
                        else:
                            prev = nn
            traverse(node,myDict)

def insertIntoInflux(kmlfile):
    myDict = collections.defaultdict(list)
    f = ""
    dom = minidom.parse(kmlfile)
    root = dom.documentElement
    traverse(root,myDict)
    
    
    fld.append('long')
    fld.append('lat')
    
    for key,val in myDict.items():
        for e in range(0,len(myDict[key])):
            s=myDict[key][e]
            s = re.sub('\s+', '', s)
            if(not s):
                myDict[key][e]=""
    
    sum=0
    cord= myDict['coordinates']
    nocid=len(cord)
    for j in range(0,len(cord)):
        s= cord[j].split(',0.0')
        sum=sum+len(s)-1
        rl=len(s)-1
        myDict['nof'].append(rl)
        for k in range(0,rl):
            st=s[k].split(',')
            o=0
            myDict['cid'].append(j)
            for jk in range(len(st)):
                if(o==0):
                    myDict['long'].append(float(st[jk]))
                elif(o==1):
                    myDict['lat'].append(float(st[jk]))
                o=o+1
    
    nml=len(myDict['name'])
    extra=myDict['nof']
    nameMap=myDict['name']
    latMap=collections.defaultdict(list)
    longMap=collections.defaultdict(list)
    freq={}
    co=0
    for j in range(nml):
        lg=myDict['nof'][j]
        for k in range(lg):
            latMap[myDict['name'][j]].append(myDict['lat'][k+co])
            longMap[myDict['name'][j]].append(myDict['long'][k+co])
            freq[myDict['name'][j]]=lg
        co=co+lg
    
    
    
    ll=sum
    
    temp = collections.defaultdict(list)
    for key,vg in myDict.items():
        if("Data" in key and key!='Data' and key!='ExtendedData' and key!='Datanametotal'):
            f=myDict[key][0]
            cur_list= f.split('-')
            if(cur_list[1]=='map'):
                temp['map'].append(cur_list[2])
            elif(cur_list[1]=='text'):
                temp['map'].append('##')
            else:
                temp['map'].append(cur_list[1])
            temp['timeStamp'].append(cur_list[0])
            st=cur_list[3].split('_')
            latlon=cur_list[4].split('_')
            temp['posLat'].append(float(latlon[0]))
            temp['posLong'].append(float(latlon[1]))
            if(len(st)!=1):
                temp['source'].append(st[1])
                temp['destination'].append(st[2])
                temp['priority'].append(st[3])
                temp['metadata'].append(cur_list[3])
                temp['text'].append('##')
            else:
                temp['source'].append('##')
                temp['destination'].append('##')
                temp['priority'].append('##')
                temp['metadata'].append('##')
                temp['text'].append(st[0])
    noofmap = len(myDict['name'])
    
    for kk,vk in temp.items():
        l= len(temp[kk])
        for j in range(l):
            myDict[kk].append(temp[kk][j])
    
    

    fld.append('map')
    fld.append('posLat')
    fld.append('posLong')
    fld.append('source')
    fld.append('destination')
    fld.append('priority')
    fld.append('metadata')
    fld.append('text')
    fld.append('timeStamp')
    fld.append('Datanametotal')
    
    rm=[]
    for kk,vv in myDict.items():
        if("Data" in kk and kk!='Datanametotal'):
            rm.append(kk)
        tt=[]
        fg=0
        for k in range(len(myDict[kk])):
            if(myDict[kk][k]!=''):
                fg=fg+1
                tt.append(myDict[kk][k])
        if fg==0:
            myDict[kk]=tt
    
    tdict= collections.defaultdict(list)
    for kk, vv in myDict.items():
        if(len(myDict[kk])!=0):
            tdict[kk]=myDict[kk]
    
    myDict=tdict
    for u in range(len(rm)):
        myDict.pop(rm[u], None)
    
    myDict.pop('coordinates', None)
    
    
    
    for t, v in myDict.items():
        print(t,"->",v,len(myDict[t]))
    
    
    md = int(myDict['Datanametotal'][0])
    nf=len(myDict['nof'])
    cc=0
    ind=0
    print(len(myDict['long']),len(myDict['lat']))
    jk=0
    d=0
    while jk<nf or cc<md:
        d=0
        #print("DEBUG ",cc,md,myDict['map'][cc])
        if(cc<md and myDict['map'][cc]!='##' and myDict['map'][cc]!='audio' and myDict['map'][cc]!='video' and myDict['map'][cc]!='image'):
            d= freq[myDict['map'][cc]]
        print("d = ", d,"jk = ",jk)
        g=0
        if(cc<md):
            if(myDict['text'][cc]!='##' or myDict['map'][cc]=='audio' or myDict['map'][cc]=='video' or myDict['map'][cc]=='image'):
                g=g+1
        if(g==1):
            dc={}
            for kk,vt in myDict.items():
                if(kk=='long' or kk=='lat'):
                    dc[kk]=0.000000000000
                elif(kk=='cid'):
                    continue
                elif kk=='Datanametotal':
                    dc[kk]=myDict[kk][0]
                elif(kk=='styleUrl' or kk=='name' or kk=='nof'):
                    continue
                else:
                    if(myDict[kk][cc]!='##'):
                        dc[kk]=myDict[kk][cc]
                    else:
                        dc[kk]=""
            print("hi1 ",dc)
            nflag=0
            tflag=0
            if(dc['metadata'] is not ""):
                mm=myclient.query('use gis')
                res = myclient.query('select distinct(metadata) from kml')
                print(res,'++++++++++++++++++++++++++++++++++')
                if(res is not None):
	                res = list(res.get_points(measurement='kml'))
	                print("1 Hi res ",len(res))
	                for met in range(len(res)):
	                    print("res[met]['metadata']=",res[met]['distinct'])
	                    print("dc['metadata']=",dc['metadata'])
	                    if res[met]['distinct'] is not None and dc['metadata'] in res[met]['distinct']:
	                        nflag=1
	                        break
            else:
                querySt=""
                print("pupul ")
                myclient.query('use gis')
                res = myclient.query('select distinct(text) from kml')
                print(res,'++++++++++++++++++++++++++++++++++')
                if(res is not None):
	                res = list(res.get_points(measurement='kml'))
	                print("2 Hi res ",len(res))
	                for met in range(len(res)):
	                    print("res[met]['distinct']=",res[met]['distinct'])
	                    print("dc['text']=",dc['text'])
	                    if res[met]['distinct'] is not None and dc['text'] in res[met]['distinct']:
	                        nflag=1
	                        querySt=dc['text']
	                        break
                # if(nflag==1):
                #     queryForm="select timeStamp from kml where text='"+querySt+"'"
                #     print(queryForm)
                #     qq=myclient.query(queryForm)
                #     qq = list(qq.get_points(measurement='kml'))
                #     print(qq)
                #     for ii in range(len(qq)):
                #         if(qq[ii]['timeStamp']==dc['timeStamp']):
                #             tflag=1
                #             break
                #         else:
                #             tflag=0
                #             nflag=0

            if(nflag==0 and tflag==0):
                print(dc)
                MySeriesHelper(**dc)
            for kk, vm in dc.items():
                print(kk, vm)
        else:
            latList=latMap[myDict['map'][cc]]
            longList=longMap[myDict['map'][cc]]
            print(latList)
            print(longList)
            for j in range(d):
                print("j = ",j)
                dc = {}
                for kk,vt in myDict.items():
                    if(kk!='long' and kk!='lat' and kk!='cid'):
                        if kk=='Datanametotal':
                            dc[kk]=myDict[kk][0]
                        elif(kk=='styleUrl' or kk=='name' or kk=='nof'):
                            continue
                        else:
                            if(myDict[kk][cc]!='##'):
                                dc[kk]=myDict[kk][cc]
                            else:
                                dc[kk]=""
                    elif(kk=='long'):
                        dc[kk]=longList[j]
                    elif(kk=='lat'):
                        dc[kk]=latList[j]
                    elif(kk=='cid'):
                        continue
                nflag=0
                print("hi ",dc)
                if(dc['metadata'] is not ""):
                	er="hi there "
                	myclient.query('use gis')
                	res=myclient.query('select count(metadata) from kml where metadata='+dc['metadata']+"'")
                	print(res,'++++++++++++++++++++++++++++++++++')
                	if(res is not None):
	                	res = list(res.get_points(measurement='kml'))
	                	print("hey hey ",len(res))
	                	counter=0
	                	for met in range(len(res)):
	                		counter=res[met]['count']
	                		break
	                	print("counter ",count)
	                	if(counter==len(extra)):
	                		nflag=1
                if(nflag==0):
                	MySeriesHelper(**dc)
                # nflag=0
                # if(dc['metadata'] is not ""):
                #     res = myclient.query('select distinct(metadata) from kml')
                #     res = list(res.get_points(measurement='kml'))
                #     for met in range(len(res)):
                #         print("res[met]['metadata']=",res[met]['distinct'])
                #         print("dc['metadata']=",dc['metadata'])
                #         if res[met]['distinct'] is not None and dc['metadata'] in res[met]['distinct']:
                #             nflag=1
                #             break
                # if(nflag==0):
                MySeriesHelper(**dc)
                for kk,vm in dc.items():
                    print(kk,vm)
    
            jk=jk+1
    
            ind = ind + d
        print("ind = ",ind)
        cc=cc+1
    print("Chnadrika Mukherjee")
    
    result= myclient.query('select * from kml_data')
    print(result)



class Watcher:
    DIRECTORY_TO_WATCH =sys.argv[1]

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        i=0
        if event.is_directory:
            return None

        elif event.event_type == 'created' or event.event_type == 'modified':
            # Take any action here when a file is first created.
            i=i+1
            path=event.src_path
            if(path.endswith('.kml')):
                flag=0
                try:
                    tree=minidom.parse(path)
                    root=tree.documentElement
                except:
                    flag=1
                if(flag==1):
                    print(path," is not validated file ")
                else:
                    print("hi now ",path)
                    insertIntoInflux(path)








w = Watcher()
w.run()




            






