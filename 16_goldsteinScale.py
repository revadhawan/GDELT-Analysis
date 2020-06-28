#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
from sklearn.cluster import KMeans

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
events = coll.aggregate([{'$sample': { 'size': 100 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# 05. GOLDSTEIN SCALE AVERAGE BY COUNTRIES
df['GoldsteinScale'] = df['GoldsteinScale'].astype(float)
df.groupby('Actor1CountryCode')['GoldsteinScale'].mean().plot(kind='barh')
plt.title('GOLDSTEIN SCALE PER MONTH')
plt.ylabel('Goldstein scale')
plt.xlabel('')
show()