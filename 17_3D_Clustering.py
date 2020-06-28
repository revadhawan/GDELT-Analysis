import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
# events = coll.find(no_cursor_timeout=True).limit(3000000)
events = coll.aggregate([{'$sample': { 'size': 100000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df[df['GoldsteinScale'].notna()]
print(df['EventRootCode'].count())
print(df['GoldsteinScale'].count())
print(df['AvgTone'].count())

# K-MEANS
v1 = pd.to_numeric(df['EventRootCode']).values
v2 = pd.to_numeric(df['GoldsteinScale']).values
# v3 = pd.to_numeric(df['AvgTone']).values
v3 = pd.to_numeric(df['NumMentions']).values


x1 = np.array(v1)
x2 = np.array(v2)
x3 = np.array(v3)

X = np.array(list(zip(x1, x2, x3)))
X.shape

km = KMeans(n_clusters=3)
km.fit(X)
km.predict(X)
labels = km.labels_

#Plotting
fig = plt.figure(1, figsize=(7,7))
ax = Axes3D(fig, rect=[0, 0, 0.95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2],
          c=labels.astype(np.float), edgecolor="k", s=50)
ax.set_xlabel("Event Root Code")
ax.set_ylabel("Goldstein Scale")
ax.set_zlabel("Num mentions")
plt.title("K Means", fontsize=14)
show() 