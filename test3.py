import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
from sklearn.cluster import KMeans

import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

# importing the statistics module 
from statistics import stdev 
  
# importing frations as parameter values 
from fractions import Fraction as fr 

# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
# events = coll.find({'MonthYear': '202001' }, no_cursor_timeout=True).limit(1000)
events = coll.aggregate([{'$match': {'MonthYear': '202001'}},{'$sample': { 'size': 100000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# MEASURES (INPUTS)
v1 = pd.to_numeric(df['GoldsteinScale']).values
v2 = pd.to_numeric(df['AvgTone'], errors='coerce').values

x1 = np.array(v1)
x2 = np.array(v2)

# CREATE COORDINATES WITH THE INPUTS (x,y)
X = np.array(list(zip(x1, x2)))
X.shape

# ASSIGNING NUMBER OF CLUSTERS FOR KMEANS
kmeans = KMeans(n_clusters=3)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

colors=["m.", "r.", "c.", "y.", "b."]

# print(X)

# SEPARATING VALUES FOR DIFFERENT CLUSTERS
def groupby(X, labels):
    sidx = labels.argsort(kind='mergesort')
    X_sorted = X[sidx]
    labels_sorted = labels[sidx]
    
    cut_idx = np.flatnonzero(np.r_[True, labels_sorted[1:] != labels_sorted[:-1], True])
    
    out = [X_sorted[i:j] for i,j in zip(cut_idx[:-1],cut_idx[1:])]
    return out

result = groupby(X, labels)

for cluster in result:
    for i in range(len(cluster)):
        sums = cluster[i][0] + cluster[i][1]

    print('Max values:', max(cluster, key=lambda x: x[0] + x[1] ))
    print('Min values:', min(cluster, key=lambda x: x[0] + x[1] ))
    print('Standard Deviation for x:', (stdev(cluster[:,0])))
    print('Standard Deviation for y:', (stdev(cluster1[:,1])))


for i in range(len(X)):
    # print("Coordenate: ", X[i], "Label: ", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=150, linewidths=5, zorder=10)
# dend = sch.dendrogram(sch.linkage(X, method='ward'))
plt.xlabel('Goldstein Scale')
plt.ylabel('AvgTone')
plt.title('Clustering')
plt.show()

# AVERAGE VALUE
print('Mean:', np.mean(x1))

# CENTROIDS VALUES
print("Centroids:", centroids)
    
    
    


           