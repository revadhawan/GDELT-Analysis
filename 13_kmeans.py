import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
from sklearn.cluster import KMeans

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
# events = coll.find(no_cursor_timeout=True).limit(3000000)
events = coll.aggregate([{'$sample': { 'size': 10000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# K-MEANS
# v1 = pd.to_numeric(df['EventRootCode'], errors='coerce').values
v1 = pd.to_numeric(df['GoldsteinScale']).values
v2 = pd.to_numeric(df['AvgTone'], errors='coerce').values
# v2 = pd.to_numeric(df['NumMentions']).values

x1 = np.array(v1)
x2 = np.array(v2)

X = np.array(list(zip(x1, x2)))
X.shape

kmeans = KMeans(n_clusters=3)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

colors=["m.", "r.", "c.", "y.", "b."]


for i in range(len(X)):
    # print("Coordenate: ", X[i], "Label: ", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=150, linewidths=5, zorder=10)
plt.xlabel('Goldstein Scale')
plt.ylabel('AvgTone')
plt.title('K-Means Clustering')
plt.show()

# Centroids value
print("Centroids:", centroids)

# Number of events
number_of_events = coll.count_documents({})
print ("Number of events:", number_of_events)

# Max values for X
max_x = max(x1)  # Find the maximum y value
max_y = x2[x1.argmax()]  # Find the x value corresponding to the maximum y value
print ("Max values for x: ")
print ("x =", max_x, "y =", max_y)

# Min values X
min_x = min(x1)  # Find the maximum y value
min_y = x2[x1.argmin()]  # Find the x value corresponding to the maximum y value
print ("Min values for x: ")
print ("x =", min_x, "y =", min_y)


# Max values for Y
max_y = max(x2)  # Find the maximum y value
max_x = x1[x2.argmax()]  # Find the x value corresponding to the maximum y value
print ("Maximum values for y: ")
print ("x =", max_x, "y =", max_y)

# Min values Y
min_y = min(x2)  # Find the maximum y value
min_x = x1[x2.argmin()]  # Find the x value corresponding to the maximum y value
print ("Min values for y: ")
print ("x =", min_x, "y =", min_y)