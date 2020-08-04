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

os.environ["PROJ_LIB"] = "D:\\Anaconda\Library\share"; #fixr


# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
# events = coll.find({'MonthYear': '202001'}, no_cursor_timeout=True)
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['US','ES','CN','BR','IN','IT','GB','RS','TU','PL'] }}}, {'$sample': { 'size': 30 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)
df = df[df['ActionGeo_CountryCode'].notna()]
df = df[df['GoldsteinScale'].notna()]


# 02. CLUSTERING
v1 = pd.Categorical(df['ActionGeo_CountryCode']).codes
x = pd.to_numeric(df['EventRootCode']).values
df['gs'] = pd.to_numeric(df['GoldsteinScale']).values

# mean = df.groupby('ActionGeo_CountryCode')['gs'].mean()
# print(mean)

mean = [0.683633, 1.295238, -0.250408, 1.018275, 0.504415, 1.085279, 0.649574, 0.581265, 0.447942, 0.654527]
countries = ['BR','CN','ES','GB','IN','IT','PL','RS','TU','US']

plt.rcParams["figure.figsize"] = (8, 8)
fig, ax = plt.subplots()
ax.bar(countries, mean, color="sandybrown")
ax.set(title="Average value for Goldstein Scale")
ax.set(xlabel="Country code", ylabel="Goldstein Scale")

plt.show()