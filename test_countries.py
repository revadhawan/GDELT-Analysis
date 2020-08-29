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
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['US','SP','CH','BR','IN','IT','UK','RS','TU','PL'] },'MonthYear': '202003'}}, {'$sample': { 'size': 2000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['ActionGeo_CountryCode'].notna()]
df['GoldsteinScale'] = pd.to_numeric(df['GoldsteinScale']).values

# 01. Goldstein Scale and avgTone
df['x'] = pd.to_numeric(df['GoldsteinScale']).values
df['y'] = pd.to_numeric(df['AvgTone']).values
df = df.filter(['ActionGeo_CountryCode','x','y'], axis=1)
df = df.groupby('ActionGeo_CountryCode').mean()

# 02. Goldstein scale and number of events
# df = df.filter(['ActionGeo_CountryCode','GoldsteinScale','_id'], axis=1)
# df = df.groupby('ActionGeo_CountryCode') \
#        .agg({'_id':'size', 'GoldsteinScale':'mean'}) \
#        .rename(columns={'_id':'y','GoldsteinScale':'x'}) \
#        .reset_index()
# total=sum(df['y'])
# df['y'] = df['y'] * 100 / total
# print(df)

# 02. Goldstein scale and number of events
# df = df.filter(['ActionGeo_CountryCode','GoldsteinScale','_id'], axis=1)
# df = df.groupby('ActionGeo_CountryCode') \
#        .agg({'_id':'size', 'GoldsteinScale':'mean'}) \
#        .rename(columns={'_id':'y','GoldsteinScale':'x'}) \
#        .reset_index()
# g = df['EventRootCode'] ='02'
# event02 = df['g']
# print(event02)


# 03. Goldstein scale and number of cases
# df['x'] = pd.to_numeric(df['GoldsteinScale']).values
# df = df.filter(['ActionGeo_CountryCode','x'], axis=1)
# df = df.groupby('ActionGeo_CountryCode').mean()
# # countries = ['BR','CH','IN','IT','PL','RS','SP','TU','UK','US']
# df['y'] = [1408485, 83531, 585792, 240599, 34393, 647849, 272829, 199906, 283253, 2729470]
# print(df)

# MEASURES (INPUTS)
x1 = np.array(df['x'])
x2 = np.array(df['y'])
n = list(df.groupby('ActionGeo_CountryCode').groups.keys())

# CREATE COORDINATES WITH THE INPUTS (x,y)
X = np.array(list(zip(x1, x2)))
X.shape

# ASSIGNING NUMBER OF CLUSTERS FOR KMEANS
kmeans = KMeans(n_clusters=3)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

colors=["m.", "r.", "c.", "y.", "b."]


# 01. SEPARATING VALUES FOR DIFFERENT CLUSTERS
def groupby(X, labels):
    sidx = labels.argsort(kind='mergesort')
    X_sorted = X[sidx]
    labels_sorted = labels[sidx]
    
    cut_idx = np.flatnonzero(np.r_[True, labels_sorted[1:] != labels_sorted[:-1], True])
    
    out = [X_sorted[i:j] for i,j in zip(cut_idx[:-1],cut_idx[1:])]
    return out

result = groupby(X, labels)

# 02. CALCULATIONS FOR EACH CLUSTER
for cluster in result:
    for i in range(len(cluster)):
        sums = cluster[i][0] + cluster[i][1]

    print('Max values:', max(cluster, key=lambda x: x[0] + x[1] ))
    print('Min values:', min(cluster, key=lambda x: x[0] + x[1] ))
    print('Standard Deviation for x:', (stdev(cluster[:,0])))
    print('Standard Deviation for y:', (stdev(cluster[:,1])))

# AVERAGE VALUE
print('Mean x:', np.mean(x1))
print('Mean y:', np.mean(x2))

# CENTROIDS VALUES
print("Centroids:", centroids)

# 03. PLOTTING THE CLUSTERS
for i in range(len(X)):
    # print("Coordenate: ", X[i], "Label: ", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=20, linewidths=5, zorder=10, color='k')
plt.xlabel('Goldstein scale')
plt.ylabel('Average tone')
# plt.title('Countries clustering')

for x1,x2,txt in np.broadcast(x1,x2,n):
    plt.annotate(txt, (x1,x2))

plt.show()
