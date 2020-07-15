#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering


client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
events = coll.aggregate([{'$match': {'MonthYear': '202001'}}, {'$sample': { 'size': 100 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# AGGLOMERATIVE (HIER)

# Variables
# X = pd.to_numeric(df['AvgTone']).values
# columns = df[['EventRootCode', 'AvgTone']].values

# K-MEANS
# v1 = pd.to_numeric(df['EventRootCode'], errors='coerce').values
v1 = pd.to_numeric(df['GoldsteinScale']).values
v2 = pd.to_numeric(df['AvgTone'], errors='coerce').values
# v2 = pd.to_numeric(df['NumMentions']).values

x1 = np.array(v1)
x2 = np.array(v2)

X = np.array(list(zip(x1, x2)))
X.shape

plt.figure(figsize=(10, 7))
plt.title("Customer Dendograms")
dend = sch.dendrogram(sch.linkage(X, method='ward'))
show()