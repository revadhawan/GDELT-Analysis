# importing frations as parameter values 
from fractions import Fraction as fr
# importing the statistics module 
from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import seaborn as sb
from matplotlib.pyplot import axis, pie, show
from pymongo import MongoClient
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans

# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
# events = coll.find({'MonthYear': '202001' }, no_cursor_timeout=True)
events = coll.aggregate([{'$match': {'MonthYear': '202006'}},{'$sample': { 'size': 300000}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['AvgTone'].notna()]
df = df[df['GoldsteinScale'].notna()]

# MEASURES (INPUTS)
v1 = pd.to_numeric(df['EventRootCode'], errors='coerce').values
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

# HIEARCHICAL CLUSTERING
# dend = sch.dendrogram(sch.linkage(X, method='ward'))
# plt.title('Dendogram')
# plt.show()

# K-MEANS CLUSTERING

# 01. SEPARATING VALUES FOR DIFFERENT CLUSTERS
# def groupby(X, labels):
#     sidx = labels.argsort(kind='mergesort')
#     X_sorted = X[sidx]
#     labels_sorted = labels[sidx]
    
#     cut_idx = np.flatnonzero(np.r_[True, labels_sorted[1:] != labels_sorted[:-1], True])
    
#     out = [X_sorted[i:j] for i,j in zip(cut_idx[:-1],cut_idx[1:])]
#     return out

# result = groupby(X, labels)

# 02. CALCULATIONS FOR EACH CLUSTER
# for cluster in result:
#     for i in range(len(cluster)):
#         sums = cluster[i][0] + cluster[i][1]

#     print('Max values:', max(cluster, key=lambda x: x[0] + x[1] ))
#     print('Min values:', min(cluster, key=lambda x: x[0] + x[1] ))
#     print('Standard Deviation for x:', (stdev(cluster[:,0])))
#     print('Standard Deviation for y:', (stdev(cluster[:,1])))

# # AVERAGE VALUE
# print('Mean x:', np.mean(x1))
# print('Mean y:', np.mean(x2))

# # CENTROIDS VALUES
# print("Centroids:", centroids)

# 03. PLOTTING THE CLUSTERS
for i in range(len(X)):
    # print("Coordenate: ", X[i], "Label: ", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=20, linewidths=5, zorder=10, color='k')
plt.xlabel('Kind of event')
plt.ylabel('Goldstein Scale')
# plt.title('Clustering')
plt.show()


