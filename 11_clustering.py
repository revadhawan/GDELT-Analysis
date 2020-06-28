#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
from sklearn.cluster import KMeans

from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
events = coll.aggregate([{'$sample': { 'size': 100000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)


# K-MEANS
 
# Variables
x = pd.to_numeric(df['EventRootCode']).values
y = pd.to_numeric(df['GoldsteinScale']).values

# print('Mean value for AvgTone:', pd.to_numeric(df['AvgTone'], errors='coerce').mean())
info= df[['GoldsteinScale', 'EventRootCode']].to_numpy()

X = np.array(list(zip(x,y)))
# print(X)

kmeans = KMeans(n_clusters=3)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

colors=["m.", "r.", "c.", "y.", "b."]

for i in range(len(X)):
    # print("Coordenate: ", X[i], "Label: ", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=150, linewidths=5, zorder=10)
plt.show()
