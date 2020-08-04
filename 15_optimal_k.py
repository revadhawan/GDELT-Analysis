import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
from sklearn.cluster import KMeans

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
# events = coll.find(no_cursor_timeout=True).limit(3000000)
events = coll.aggregate([{'$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# K-MEANS
 
# Variables
X = np.array(df[['EventRootCode']])
y = np.array(df[['AvgTone']])
X.shape

# print('Mean value for AvgTone:', pd.to_numeric(df['GoldsteinScale'], errors='coerce').mean())
# print('Mean value for AvgTone:', pd.to_numeric(df['GoldsteinScale'], errors='coerce').min())

Nc = range(1, 10)
kmeans = [KMeans(n_clusters=i) for i in Nc]
kmeans
score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
score
plt.plot(Nc,score)
plt.grid()
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()

