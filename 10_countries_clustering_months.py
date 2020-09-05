from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.cluster import KMeans

# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['BR','CH','IN','IT','PL','RS','SP','TU','UK','US'] }}}, {'$sample': { 'size': 500000}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

grouped = df.groupby('MonthYear')
for name, df in grouped:
    # Remove rows with NaN values
    df = df.replace('null', np.nan, regex=True)
    df = df[df['ActionGeo_CountryCode'].notna()]

    # 01. Goldstein scale and average tone
    df['x'] = pd.to_numeric(df['GoldsteinScale']).values
    df['y'] = pd.to_numeric(df['AvgTone']).values
    df = df.filter(['ActionGeo_CountryCode','x','y'], axis=1)
    df = df.groupby('ActionGeo_CountryCode').mean()

    # MEASURES (INPUTS)
    x1 = np.array(df['x'])
    x2 = np.array(df['y'])
    n = list(df.groupby('ActionGeo_CountryCode').groups.keys())

    # CREATE COORDINATES WITH THE INPUTS (x,y)
    X = np.array(list(zip(x1, x2)))
    X.shape
    
    # Centroids for ten selected countries (commment if using all countries)
    centroids = np.array([[0.45,-2.95], [0.86,-2.54], [0.95,-1.55]], np.float64)
    # Centroids for all countries (commment if using ten countries)
    centroids = np.array([[-0.37,-3.61], [0.93, -2.07], [1.61,-0.62]], np.float64)

    # ASSIGNING NUMBER OF CLUSTERS FOR KMEANS
    kmeans = KMeans(n_clusters=3, init=centroids, n_init=1)
    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
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

        print('Percentage of events:', len(cluster)*100 / len(n))
        print('Min values:', min(cluster, key=lambda x: x[0] + x[1]))
        print('Max values:', max(cluster, key=lambda x: x[0] + x[1]))    
        print('Standard Deviation for x:', (stdev(cluster[:,0])))
        print('Standard Deviation for y:', (stdev(cluster[:,1])))
        print("\n")

    # AVERAGE VALUE
    print('Mean x:', np.mean(x1))
    print('Mean y:', np.mean(x2))
    print("\n")

    # CENTROIDS VALUES
    print("Centroids:", centroids)

    # 03. PLOTTING THE CLUSTERS
    for i in range(len(X)):
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
    plt.scatter(centroids[:,0], centroids[:,1], marker='.', s=20, linewidths=5, zorder=10, color='k')
    plt.xlabel('Goldstein scale')
    plt.ylabel('Average tone')

    for x1,x2,txt in np.broadcast(x1,x2,n):
        plt.annotate(txt, (x1,x2))

    plt.title(name)
    # Range for ten countries (commment if using all countries)
    plt.xlim(0,1.3)
    plt.ylim(-4.5, -1)
    # Range for all countries (commment if using ten countries)
    plt.xlim(-8,8)
    plt.ylim(-7,4)
    
    plt.show()