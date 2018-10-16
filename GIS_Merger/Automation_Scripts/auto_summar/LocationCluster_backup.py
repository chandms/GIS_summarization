import os
from copy import deepcopy
from sklearn.metrics import silhouette_score
import csv
from sklearn.datasets import load_iris
import numpy as np
#import matplotlib.ticker as ticker
import pandas as pd
import pickle
#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
def ClusterFunc(data):
     f1=[]
     f2=[]
     f4=[]
     f5=[]
     #print(data)
     for i in range(len(data)):
          if data[i]['text']: 
               f1.append(float(data[i]['posLat']))
               f2.append(float(data[i]['posLong']))
               f4.append(data[i]['timeStamp'])
               f5.append(data[i]['text'])
     tvalue=data[i]['time']
     mm=[]
     sil=[]
     cnt=0
     X = np.array(list(zip(f1, f2)))
     def dist(a, b, ax=1):
         return np.linalg.norm(a - b, axis=ax)
     for n_cluster in range(2, 5):
         kmeans = KMeans(n_clusters=n_cluster).fit(X)
         label = kmeans.labels_
         print(label)
         sil_coeff = silhouette_score(X, label, metric='manhattan')
         mm.append(sil_coeff)
     #print("mm",mm)
     k=mm.index(max(mm))+2
     #print ('optimal number of clusters :',k)
     C_x = np.random.randint(0, np.max(X)-20, size=k)
     C_y = np.random.randint(0, np.max(X)-20, size=k)
     C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
     C_old = np.zeros(C.shape)
     clusters = np.zeros(len(X))
     error = dist(C, C_old, None)
     kmeans = KMeans(n_clusters=k)
     kmeans = kmeans.fit(X)
     labels = kmeans.predict(X)
     labels2=kmeans.labels_
     centroids = kmeans.cluster_centers_
     centroids=centroids.tolist()
     jj=[]
     c_data=[]
     #writer.writerow(['Message','cluster_number'])
     for i in range(len(X)):
         c_data.append([f5[i],(labels2[i]+1),f1[i],f2[i],f4[i]])
     return c_data,tvalue,centroids
##     pl=['1','2','3','4','5','6','7','8','9','10']
##     fig = plt.figure()
##     ax = fig.add_subplot(111, projection='3d')
##     ax.locator_params(nbins=1,axis='z')
##     colors = ['r', 'g', 'b', 'y', 'c', 'm','Orange','ForestGreen','Brown','peachpuff','gold','rosybrown']
##     ax.scatter(f1, f2, c='blue', s=9)
##     sc=ax.scatter(X[:,0],X[:,1],1,c=labels2,s=100,depthshade='True',marker=".")
##     ax.scatter(centroids[:,0],centroids[:,1],1,c='black',s=200,depthshade='True',marker="D")
##     ax.set_zlim(1,1.01)
##     plt.colorbar(sc)
##     plt.show()
##     print("Final centroids")
##     print(centroids)

