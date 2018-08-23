import re
import time,os
from xml import dom
from influxdb import InfluxDBClient
from xml.dom.minidom import Node
from xml.dom import minidom
import collections
from influxdb import SeriesHelper



fld=[]



myclient = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', database='gis')

myclient.create_database('gis')
myclient.create_retention_policy('awesome_policy', '30d', '3', default=True)


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
                    else:
                        name = dom.getElementsByTagName('value')
                        myDict[f].append(name[0].firstChild.nodeValue)
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
    
    
    for key,v in myDict.items():
        fld.append(key)
    
    
    fld.append('long')
    fld.append('lat')
    fld.remove('coordinates')
    
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
            print(st, len(st))
            o=0
            myDict['cid'].append(j)
            for jk in range(len(st)):
                if(o==0):
                    myDict['long'].append(float(st[jk]))
                elif(o==1):
                    myDict['lat'].append(float(st[jk]))
                o=o+1
    
    nml=len(myDict['name'])
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
                temp['map'].append('')
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
                temp['metadata'].append(st[4])
                temp['text'].append('')
            else:
                temp['source'].append('')
                temp['destination'].append('')
                temp['priority'].append('')
                temp['metadata'].append('')
                temp['text'].append(st[0])
    noofmap = len(myDict['name'])
    
    for kk,vk in temp.items():
        l= len(temp[kk])
        for j in range(l):
            myDict[kk].append(temp[kk][j])
    
    
    fld.append('nof')
    fld.append('map')
    fld.append('posLat')
    fld.append('posLong')
    fld.append('source')
    fld.append('destination')
    fld.append('priority')
    fld.append('metadata')
    fld.append('text')
    fld.append('timeStamp')
    
    rm=[]
    for kk,vv in myDict.items():
        if("Data" in kk and kk!='Datanametotal'):
            fld.remove(kk)
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
    
    
    
    
    
    for t, v in myDict.items():
        print(t,"->",v,len(myDict[t]))
    myDict.pop('coordinates', None)
    
    md = int(myDict['Datanametotal'][0])
    nf=len(myDict['nof'])
    cc=0
    ind=0
    print(len(myDict['long']),len(myDict['lat']))
    jk=0
    d=0
    while jk<nf or cc<md:
        d=0
        if(cc<md and myDict['map'][cc]!='' and myDict['map'][cc]!='audio' and myDict['map'][cc]!='video' and myDict['map'][cc]!='image'):
            d= freq[myDict['map'][cc]]
        print("d = ", d,"jk = ",jk)
        g=0
        if(cc<md):
            if(myDict['text'][cc]!='' or myDict['map'][cc]=='audio' or myDict['map'][cc]=='video' or myDict['map'][cc]=='image'):
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
                    if(myDict[kk][cc]!=''):
                        dc[kk]=myDict[kk][cc]
                    else:
                        dc[kk]="........"
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
                            if(myDict[kk][cc]!=''):
                                dc[kk]=myDict[kk][cc]
                            else:
                                dc[kk]="........"
                    elif(kk=='long'):
                        dc[kk]=longList[j]
                    elif(kk=='lat'):
                        dc[kk]=latList[j]
                    elif(kk=='cid'):
                        continue
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


path_to_watch = "/home/chandrika/Desktop/GIS_summarization/kmlFiles/"
before = dict()
print("before ",dict)
while 1:
    time.sleep(2)
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print("after ",dict)
        print("Added: ", ", ".join(added))
        ll = len(added)
        for zk in range(ll):
            dir = path_to_watch
            fname = os.path.join(dir, added[zk])
            print("hi now ",fname)
            insertIntoInflux(fname)
    else:
        print("Nothing changed")
    before=after
            






