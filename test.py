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
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['UK'] }}}, {'$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df[df['ActionGeo_CountryCode'].notna()]

print(df)