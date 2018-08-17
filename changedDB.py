import re
import xmltodict
from influxdb import InfluxDBClient
import xml.dom.minidom as  md
from xml.dom.minidom import Node
from xml.dom import minidom
import pandas as pd
import json
import collections
from influxdb import SeriesHelper
import xml.etree.ElementTree as ET
from influxdb import DataFrameClient
from ast import literal_eval

headList =[]
fld=[]
myDict = collections.defaultdict(list)
f=""


myclient = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', database='chandrika')

myclient.create_database('chandrika')
myclient.create_retention_policy('awesome_policy', '3d', '3', default=True)
#myclient = InfluxDBClient(host='127.0.0.1', port=8086)


class MySeriesHelper(SeriesHelper):
    # """Instantiate SeriesHelper to write points to the backend."""

    class Meta:
        # """Meta class stores time series helper configuration."""

        # The client should be an instance of InfluxDBClient.
        client = myclient

        # The series name must be a string. Add dependent fields/tags
        # in curly brackets.
        series_name = 'kml_data'

        # Defines all the fields in this time series.
        fields = fld

        # Defines all the tags for the series.
        tags = []

        # Defines the number of data points to store prior to writing
        # on the wire.
        bulk_size = 0

        autocommit= True

def traverse(root):
    global f
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                if(node.tagName=="Style"):
                    continue
                    # ln=''
                    # for elem in node.attributes.values():
                    #     ln=ln+elem.firstChild.data
                    # y=0
                    # for cn in node.childNodes:
                    #     if(y==1):
                    #         rt=0
                    #         for kn in cn.childNodes:
                    #             if rt==0:
                    #                 myDict["LineColor"].append(ln+"_"+kn.wholeText)
                    #             elif(rt==1):
                    #                 myDict["width"].append(kn.wholeText)
                    #             rt=rt+1
                    #     elif(y==4):
                    #         for kn in cn.childNodes:
                    #             myDict["PolyColor"].append(kn.wholeText)
                    #
                    #     y=y+1
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
            traverse(node)

def collect(root):
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                headList.append(node.tagName)
                if (node.hasAttributes()):
                    r=list(node.attributes.keys())[0]
                    f= node.tagName+r
                    for elem in node.attributes.values():
                        f=f+elem.firstChild.data
                    headList.append(f)
            collect(node)



kmlfile='C:/Users/Pupul/Desktop/kml/cur1.kml'
dom = md.parse(kmlfile)
root = dom.documentElement
team = dom.documentElement
collect(root)
headSet=set(headList)
print(headSet)

traverse(root)

for key,v in myDict.items():
    print(key+"-> ")
    fld.append(key)
    for l in range(0,len(myDict[key])):
        print(myDict[key][l])

print("printing field")
fld.append('long')
fld.append('lat')
fld.remove('coordinates')
print(fld)
for key,val in myDict.items():
    for e in range(0,len(myDict[key])):
        s=myDict[key][e]
        s = re.sub('\s+', '', s)
        if(not s):
            myDict[key][e]=""
    if("" in myDict[key]):
        myDict[key].remove("")


ll=0
for key,vl in myDict.items():
    fd=len(myDict[key])
    if(fd>ll):
        ll=fd
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

print("sum = ",sum)
ll=sum

temp = collections.defaultdict(list)
for key,vg in myDict.items():
    if("Data" in key and key!='Data' and key!='ExtendedData' and key!='Datanametotal'):
        f=myDict[key][0]
        cur_list= f.split('-')
        if(cur_list[1]=='map'):
            temp['map'].append(cur_list[2])
        else:
            temp['map'].append('')
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

fld.append('cid')
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




cc=0
p=0

for t, v in myDict.items():
    print(t,"->",v,"cm")
myDict.pop('coordinates', None)
for j in range(nocid):
    d= myDict['nof'][j]

    for j in range(d):
        dc = {}
        for kk,vv in myDict.items():
            if(kk!='long' and kk!='lat'):
                if kk=='Datanametotal':
                    dc[kk]=myDict[kk][0]
                elif(kk=='styleUrl' or kk=='name' or kk=='nof' or kk=='cid'):
                    continue
                else:
                    dc[kk]=myDict[kk][cc]
            elif(kk=='long'):
                dc[kk]=myDict[kk][j]
            elif(kk=='lat'):
                dc[kk]=myDict[kk][j]
        MySeriesHelper(**dc)
    cc=cc+1




