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
                if(node.tagName=="LineStyle"):
                    #ss= dom.getElementsByTagName('LineStyle')
                    y=0
                    for cn in node.childNodes:
                        if(y==0):
                            ds=dom.getElementsByTagName('color')
                            myDict[node.tagName].append(ds[0].firstChild.nodeValue)
                        y=y+1
                elif(node.tagName=="PolyStyle"):
                    #ss= dom.getElementsByTagName('PolyStyle')
                    y = 0
                    for cn in node.childNodes:
                        if (y == 0):
                            ds = dom.getElementsByTagName('color')
                            myDict[node.tagName].append(ds[0].firstChild.nodeValue)
                        y = y + 1
                elif(node.tagName=='color'):
                    continue
                if(node.tagName=="Data"):
                    f="Data"+list(node.attributes.keys())[0]
                    for elem in node.attributes.values():
                        f=f+elem.firstChild.data
                    if(node.hasChildNodes()):
                        y = 0
                        for cn in node.childNodes:
                            if (y == 0):
                                ds = dom.getElementsByTagName('value')
                                myDict[f].append(ds[0].firstChild.nodeValue)
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



kmlfile='C:/Users/Pupul/Desktop/kml/1234.kml'
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
    if(len(myDict[key])==0):
        myDict[key].apppend("emp")
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


ll=0
for key,vl in myDict.items():
    fd=len(myDict[key])
    if(fd>ll):
        ll=fd
sum=0
cord= myDict['coordinates']
for j in range(0,len(cord)):
    s= cord[j].split(',0.0')
    sum=sum+len(s)-1
    rl=len(s)-1
    for k in range(0,rl):
        st=s[k].split(',')
        print(st, len(st))
        o=0
        for j in range(len(st)):
            if(o==0):
                myDict['long'].append(float(st[j]))
            elif(o==1):
                myDict['lat'].append(float(st[j]))
            o=o+1

print("sum = ",sum)
ll=sum
myDict.pop('coordinates', None)
for k in range(0,ll):
    dc={}
    for km, vm in myDict.items():
        l=len(myDict[km])
        if(l!=ll and l is not 0):
            dc[km]=myDict[km][0]
        elif(l!=ll and l is  0):
            dc[km]=""
        else:
            dc[km]=myDict[km][k]
    for r, y in dc.items():
        print(r,y)
    MySeriesHelper(**dc)



