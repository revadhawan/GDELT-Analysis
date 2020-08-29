import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

from mpl_toolkits.mplot3d import Axes3D
from statistics import stdev
from scipy.cluster.vq import kmeans
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
# events = coll.find(no_cursor_timeout=True).limit(3000000)
events = coll.aggregate([{'$sample': { 'size': 3000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['GoldsteinScale'].notna()]
df['GoldsteinScale'] = pd.to_numeric(df['GoldsteinScale']).values

# K-MEANS
v1 = pd.to_numeric(df['EventRootCode']).values
v2 = pd.to_numeric(df['GoldsteinScale']).values
v3 = pd.to_numeric(df['AvgTone']).values

# MEASURES (INPUTS)
x1 = np.array(v1)
x2 = np.array(v2)
x3 = np.array(v3)

# CREATE COORDINATES WITH THE INPUTS (x,y)
X = np.array(list(zip(x1, x2, x3)))
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

    print('Max values:', max(cluster, key=lambda x: x[0] + x[1] + x[2]))
    print('Min values:', min(cluster, key=lambda x: x[0] + x[1] + x[2]))
    print('Standard Deviation for x:', (stdev(cluster[:,0])))
    print('Standard Deviation for y:', (stdev(cluster[:,1])))
    print('Standard Deviation for z:', (stdev(cluster[:,2])))

# AVERAGE VALUE
print('Mean x:', np.mean(x1))
print('Mean y:', np.mean(x2))
print('Mean y:', np.mean(x3))

# CENTROIDS VALUES
print("Centroids:", centroids)

#Plotting
fig = plt.figure(1, figsize=(7,7))
ax = Axes3D(fig, rect=[0, 0, 0.95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2],
          c=labels.astype(np.float), edgecolor="k", s=50)
ax.set_xlabel("Event Root Code")
ax.set_ylabel("Goldstein Scale")
ax.set_zlabel("Average Tone")
plt.title("K Means", fontsize=14)
show() 