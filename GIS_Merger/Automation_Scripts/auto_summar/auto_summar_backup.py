from influxdb import InfluxDBClient

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from sumy.summarizers.lex_rank import LexRankSummarizer

from LocationCluster import ClusterFunc

import datetime
import time as t
from datetime import timezone

try:
    client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='gis')
except:
    print("Influxdb Error")

##try:
##    client.create_database('kml1')
##except:
##    pass

while True:
    presult= client.query('select * from parameter_table;')
    presult=list(presult.get_points(measurement='parameter_table'))
    if presult:
        for i in range(len(presult)):
            blevel=presult[i]['blevel']
            lsummary=presult[i]['lsummary']
            window=presult[i]['window']
    else:
        blevel='High'
        lsummary=2
        window=5



    tvalue = client.query('select * from tvalue;')
    tvalue=list(tvalue.get_points(measurement='tvalue'))
    for i in range(len(tvalue)):
        tvalue=tvalue[i]['last_tvalue']
    http_text=''
    #print("tvalue",tvalue)
    if tvalue:
        squery='select count(text) from kml where time > '+ str(tvalue) + ';'
        rcount=client.query(squery)
        #print(rcount)
        rcount=list(rcount.get_points(measurement='kml'))
        for i in range(len(rcount)):
            rcount=rcount[i]['count']
        #print(rcount)
        if rcount:
            if int(rcount)>int(window):
                squery='select * from kml where time > '+ str(tvalue) + ';'
                result=client.query(squery,epoch='ns')
                text=list(result.get_points(measurement='kml'))
##                for i in range(len(text)):
##                    http_text=http_text+str(text[i]['Text'])+'. '
                
                c_data=[]
                c_data,last_tvalue,centroids=ClusterFunc(text)
                #print("centroids",centroids)
                #print(c_data)
                #last_tvalue=text[len(text)-1]['time']
                time=datetime.datetime.utcnow()
                data = [
                {
                    "measurement": "tvalue",
                    "time": str(time),
                    "fields": {
                        "last_tvalue":last_tvalue,
                    }
                }
                ]
                client.query('drop measurement tvalue')
                client.write_points(data)
                #client.query(squery)
                #print(http_text)
                clusters=[]
                for data in c_data:
                    clusters.append(data[1])
                #print("clusters",clusters)
                clustered_summary=[]
                #print("set length",set(clusters))
                c=1
                for i in range(len(set(clusters))):
                    corpus=''
                    for j in c_data:
                        #print(j)
                        #time=datetime.datetime.utcnow()
                        #print("Latitude",j[2])
                        #print("Longitude",j[3])
                        #print("Text",j[0])
                        if j[1]==i+1 and j[0]:
                            time=datetime.datetime.strptime(j[4], '%Y%m%d%H%M%S')
                            #print(j[4])
                            #print(time)
                            data = [
                            {
                                "measurement": "mapdata",
                                "time": str(time),
                                "fields": {
                                    "lat":j[2],
                                    "long":j[3],
                                    "text":j[0],
                                    "value":5
                                }
                            }
                            ]
                            print("points",data)
                            client.write_points(data)
                            #time=j[4]
                            with open('/home/up2/gis_test/fold/clustermap.geojson','a+') as map_file:
                                map_file.write(str(j[2])+"%"+str(j[3])+"%"+str(j[0])+"%"+"5"+"%"+str(c)+"\n") #lat long text value clustercount
                            corpus=corpus+str(j[0])+'. '
                    #print("===========================================================")
                    #print("Corpus",corpus)
                    LANGUAGE = "english"
                    SENTENCES_COUNT = lsummary
                    parser = PlaintextParser.from_string(corpus, Tokenizer(LANGUAGE))
                    stemmer = Stemmer(LANGUAGE)

                    summarizer = LexRankSummarizer(stemmer)
                    summarizer.stop_words = get_stop_words(LANGUAGE)

                    summary=summarizer(parser.document, SENTENCES_COUNT)
                    exsum=''
                    for sentence in summary:
                        exsum=exsum+" "+str(sentence)
                    time=time+datetime.timedelta(seconds=1)
                    data = [
                        {
                            "measurement": "mapdata",
                            "time": str(time),
                            "fields": {
                                "lat":centroids[i][0],
                                "long":centroids[i][1],
                                "text":exsum,
                                "value":50
                            }
                    }
                    ]
                    print("cluster data",data)
                    client.write_points(data)
                    with open('/home/up2/gis_test/fold/clustermap.geojson','a+') as map_file:
                        map_file.write(str(centroids[i][0])+"%"+str(centroids[i][1])+"%"+str(exsum)+"%"+"50"+"%"+str(c)+"\n")
                    c+=1
                    #print("Centroid Latitude",centroids[i])
                    #print("Controid Longitude",centroids[i])
                    #print("Summary",exsum)
                    clustered_summary.append([i+1,exsum.strip(),centroids[i]])

                    #print("Summary",exsum.strip())
                #print(clustered_summary)
                time=datetime.datetime.utcnow()
                data = [
                {
                    "measurement": "auto_summary",
                    "time": str(time),
                    "fields": {
                        "summary":str(clustered_summary),
                        "blevel":str(blevel),
                        "lsummary":lsummary,
                        "window":window,
                        "summary_algo":"Lex Rank",
                    }
                }
                ]
                client.write_points(data)
                

    else:
        squery='select * from kml'
        rcount=client.query(squery,epoch='ns')
        rcount=list(rcount.get_points(measurement='kml'))
        rcount=rcount[0]['time']
        time=datetime.datetime.utcnow()
        data = [
        {
            "measurement": "tvalue",
            "time": str(time),
            "fields": {
                "last_tvalue":rcount,
            }
        }
        ]
        client.write_points(data)

    t.sleep(5)


