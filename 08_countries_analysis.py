# importing frations as parameter values 
from fractions import Fraction as fr
# importing the statistics module 
from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['BR','CH','IN','IT','PL','RS','SP','TU','UK','US']}}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['AvgTone'].notna()]
df = df[df['GoldsteinScale'].notna()]
df = df[df['ActionGeo_CountryCode'].notna()]

# 01. EVOLUTION OF EVENTS DENSITY
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
df.groupby([pd.Grouper(key='SQLDATE',freq='W'),'ActionGeo_CountryCode'])['_id'].nunique().unstack('ActionGeo_CountryCode').plot()
plt.title('Number of events per country')
plt.ylabel('Number of occurrences')
plt.xlabel('Time')
show()

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

# ACTOR 1
events = coll.aggregate([{'$match': {'Actor2Geo_CountryCode': { '$in': ['BR','CH','IN','IT','PL','RS','SP','TU','UK','US'] }}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['Actor1Geo_CountryCode'].notna()]

# Actor 1
count = df.groupby('Actor1Geo_CountryCode')['_id'].count()
total=sum(count)
x = list(df.groupby('Actor1Geo_CountryCode').groups.keys())
y = count * 100 / total
print(y)

# ACTOR 2
events = coll.aggregate([{'$match': {'Actor2Geo_CountryCode': { '$in': ['BR','CH','IN','IT','PL','RS','SP','TU','UK','US'] }}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['Actor2Geo_CountryCode'].notna()]

count = df.groupby('Actor2Geo_CountryCode')['_id'].count()
x1 = list(df.groupby('Actor2Geo_CountryCode').groups.keys())
total=sum(count)
y1 = count * 100 / total
print(y1)