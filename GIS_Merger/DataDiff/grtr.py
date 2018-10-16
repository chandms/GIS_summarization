import os
import xml.dom.minidom as  md
from xml.dom.minidom import Node
import logging
import json
import xml.etree.ElementTree as ET
from collections import OrderedDict
import zipfile
from xml.dom import minidom
import os, time
from os.path import basename
from collections import defaultdict

text_list=""



def traverse(root, myDict):
    global f
    global text_list
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                if (node.tagName == "Style"):
                    continue
                elif (node.tagName == 'color' or node.tagName == 'PolyStyle' or node.tagName == 'LineStyle' or node.tagName == 'width'):
                    continue
                if (node.tagName == "Data"):
                    return
                elif (node.tagName == 'value'):
                    continue
                else:
                    prev = node
                    for nn in node.childNodes:
                        if (nn.nodeType == Node.TEXT_NODE):
                            myDict[prev.tagName].append(nn.wholeText)
                            break
                        else:
                            prev = nn
            elif node.nodeType==4:
                print(node.nodeValue)
                text_list=node.nodeValue
            traverse(node, myDict)


folder = os.listdir('./Working')
ground_truth = open("ground_truth.txt",'w')
ground_truth.write("")
ground_truth.close()
cc=0
print ("length = ",len(folder))
for file_index in range(len(folder)):
    lg=os.stat("./Working/"+folder[file_index]).st_size
    if lg==0:
        continue
    cc +=1
    current_file = folder[file_index]
    print("my current file = ",current_file)
    dom = md.parse("./Working/"+current_file)
    root = dom.documentElement
    myDict = defaultdict(list)
    global text_list
    traverse(root,myDict)

    cord = myDict['coordinates']
    nocid = len(cord)
    for j in range(0, len(cord)):
        s = cord[j].split(',0.0')
        rl = len(s) - 1
        myDict['nof'].append(rl)
        for k in range(0, rl):
            st = s[k].split(',')
            o = 0
            myDict['cid'].append(j)
            for jk in range(len(st)):
                if (o == 0):
                    myDict['long'].append(float(st[jk]))
                elif (o == 1):
                    myDict['lat'].append(float(st[jk]))
                o = o + 1


        print(str(text_list),myDict['lat'],myDict['long'])
        list_of_text = text_list.split(',')
        for tt in range(len(list_of_text)):
            ground_truth = open("ground_truth.txt",'a')
            ground_truth.write(" "+(list_of_text[tt]+":"+str(myDict['lat'])+":"+str(myDict['long'])))
            ground_truth.write("\n")
            ground_truth.close()




print (cc)


