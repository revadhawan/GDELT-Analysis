# importing frations as parameter values 
from fractions import Fraction as fr
# importing the statistics module 
from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import conda
import os
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
# events = coll.find({'MonthYear': '202001'}, no_cursor_timeout=True)
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['US','SP','CH','BR','IN','IT','UK','RS','TU','PL'] }}}, {'$sample': { 'size': 2000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)
df = df[df['ActionGeo_CountryCode'].notna()]
df = df[df['GoldsteinScale'].notna()]


# 01. GS AVERAGE
v1 = pd.Categorical(df['ActionGeo_CountryCode']).codes
x = pd.to_numeric(df['EventRootCode']).values
df['gs'] = pd.to_numeric(df['GoldsteinScale']).values

df['GoldsteinScale'] = df['GoldsteinScale'].astype(float)
y = df.groupby('ActionGeo_CountryCode')['GoldsteinScale'].mean()
x = list(df.groupby('ActionGeo_CountryCode').groups.keys())
print(x, y)
plot = df.groupby('ActionGeo_CountryCode')['GoldsteinScale'].mean().sort_values().plot(kind='bar', color='paleturquoise')


for p in plot.patches:
    plot.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=8,
                   xytext = (0, -5), 
                   textcoords = 'offset points')

plt.title('GOLDSTEIN SCALE AVERAGE')
plt.ylabel('Goldstein scale')
plt.xlabel('Country code')
plt.show()