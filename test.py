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
# events = coll.find({'MonthYear': '202001' }, no_cursor_timeout=True)
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['US','ES','CN','BR','IN','IT','GB','RS','TU','PL'] }}}, {'$sample': { 'size': 100 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df[df['ActionGeo_CountryCode'].notna()]

# K-MEANS
df['CountryCode'] = pd.Categorical(df['ActionGeo_CountryCode']).codes
v1 = pd.Categorical(df['ActionGeo_CountryCode']).codes
print(df[['CountryCode', 'ActionGeo_CountryCode']])
x = pd.to_numeric(df['GoldsteinScale']).values
y = pd.to_numeric(df['AvgTone']).values

countries = ['US','ES','CN','BR','IN','IT','GB','RS','TU','PL']

fig, ax = plt.subplots(figsize=(8,6))

for i in range(len(v1)):
    ax.scatter(x = x, y = y, c = v1, label=countries, cmap='tab20b')
plt.legend()
plt.show()
