from fractions import Fraction as fr
from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import seaborn as sb
from matplotlib.pyplot import axis, pie, show
from mpl_toolkits.mplot3d import Axes3D
from pymongo import MongoClient
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
events = coll.find(no_cursor_timeout=True).limit(20)
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['AvgTone'].notna()]
df = df[df['GoldsteinScale'].notna()]

# 01. INPUTS
v1 = pd.to_numeric(df['EventRootCode'], errors='coerce').values
v2 = pd.to_numeric(df['GoldsteinScale'], errors='coerce').values
v3 = pd.to_numeric(df['AvgTone'], errors='coerce').values

x1 = np.array(v1)
x2 = np.array(v2)
x3 = np.array(v3)

# 02. CREATE COORDINATES WITH THE INPUTS (x,y)
# X = np.array(list(zip(x1, x2)))
X = np.array(list(zip(x1, x2, x3)))
X.shape

# 03. CALCULATE OPTIMAL NUMBER OF K (CLUSTERS)
Nc = range(1, 10)
kmeans = [KMeans(n_clusters=i) for i in Nc]
kmeans
score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
score
plt.plot(Nc, score)
plt.grid()
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()

# 04. ASSIGNING NUMBER OF CLUSTERS FOR KMEANS
kmeans = KMeans(n_clusters=3)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

colors = ["m.", "r.", "c.", "y.", "b."]

# HIEARCHICAL CLUSTERING
# dend = sch.dendrogram(sch.linkage(X, method='ward'))
# plt.title('Dendogram')
# plt.show()

# K-MEANS CLUSTERING
# 05. SEPARATING VALUES FOR DIFFERENT CLUSTERS


def groupby(X, labels):
    sidx = labels.argsort(kind='mergesort')
    X_sorted = X[sidx]
    labels_sorted = labels[sidx]

    cut_idx = np.flatnonzero(
        np.r_[True, labels_sorted[1:] != labels_sorted[:-1], True])

    out = [X_sorted[i:j] for i, j in zip(cut_idx[:-1], cut_idx[1:])]
    return out


result = groupby(X, labels)

# 06. CALCULATIONS FOR EACH CLUSTER
for cluster in result:
    for i in range(len(cluster)):
        sums = cluster[i][0] + cluster[i][1]

    # 2 dimensions
    # print('Min values:', min(cluster, key=lambda x: x[0] + x[1]))
    # print('Max values:', max(cluster, key=lambda x: x[0] + x[1]))
    # print('Standard Deviation for x:', (stdev(cluster[:, 0])))
    # print('Standard Deviation for y:', (stdev(cluster[:, 1])))

    # 3 dimensions
    print('Max values:', max(cluster, key=lambda x: x[0] + x[1] + x[2]))
    print('Min values:', min(cluster, key=lambda x: x[0] + x[1] + x[2]))
    print('Standard Deviation for x:', (stdev(cluster[:, 0])))
    print('Standard Deviation for y:', (stdev(cluster[:, 1])))
    print('Standard Deviation for z:', (stdev(cluster[:, 2])))

# AVERAGE VALUE
print('Mean x:', np.mean(x1))
print('Mean y:', np.mean(x2))
print('Mean y:', np.mean(x3))

# CENTROIDS VALUES
print("Centroids:", centroids)

# 07. PLOTTING THE CLUSTERS FOR 2 DIMENSIONS
for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
plt.scatter(centroids[:, 0], centroids[:, 1], marker='x',
            s=20, linewidths=5, zorder=10, color='k')
plt.xlabel('Kind of event')
plt.ylabel('Average tone')
plt.show()

# 07. PLOTTING THE CLUSTERS FOR 3 DIMENSIONS
fig = plt.figure(1, figsize=(7, 7))
ax = Axes3D(fig, rect=[0, 0, 0.95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2],
           c=labels.astype(np.float), edgecolor="k", s=50)
ax.set_xlabel("Event Root Code")
ax.set_ylabel("Goldstein Scale")
ax.set_zlabel("Average Tone")
plt.title("K Means", fontsize=14)
show()