import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
from sklearn.cluster import KMeans

import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

# importing the statistics module 
from statistics import stdev 
  
# importing frations as parameter values 
from fractions import Fraction as fr 

# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
events = coll.find({'MonthYear': '202001' }, {'Actor1CountryCode:' 'USA', 'ESP', ''}, no_cursor_timeout=True).limit(10)
data = list(events)
events.close()
df = pd.DataFrame(data)

# MEASURES (INPUTS)
v1 = pd.to_numeric(df['GoldsteinScale']).values
v2 = pd.to_numeric(df['AvgTone'], errors='coerce').values

x1 = np.array(v1)
x2 = np.array(v2)

# CREATE COORDINATES WITH THE INPUTS (x,y)
X = np.array(list(zip(x1, x2)))
X.shape

# ASSIGNING NUMBER OF CLUSTERS FOR KMEANS
kmeans = KMeans(n_clusters=2)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_