import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show
import numpy as np

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
events = coll.find(no_cursor_timeout=True)
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['Actor1Geo_CountryCode'].notna()]
df = df[df['Actor2Geo_CountryCode'].notna()]

# 01. NUMBER OF EVENTS PER MONTH
df.groupby('MonthYear')['_id'].nunique().plot(kind='bar')
plt.title('NUMBER OF EVENTS PER MONTH')
plt.xlabel('Month')
plt.ylabel('Number of events')
show()

# 02. NUMBER EVENTS BY THEIR KIND PER MONTH
df.groupby(['MonthYear', 'EventRootCode'])[
    '_id'].nunique().unstack('MonthYear').plot(kind='bar')
plt.title('KIND OF EVENTS PER MONTH')
plt.xlabel('Event code')
plt.ylabel('Number of occurrences')
show()

# 03. TOP 5 KIND OF EVENTS WITH MOST FREQUENCY
sums = df.groupby('EventRootCode')['_id'].nunique().nlargest(5)
pie(sums, labels=sums.index, autopct='%1.1f%%')
axis('equal')
plt.title('TOP KIND OF EVENTS')
plt.xlabel('Event code')
plt.ylabel('Number of occurrences')
show()

# 04. TOP FREQUENT COUNTRIES PER MONTH (ACTOR 1)
df.groupby(['MonthYear', 'Actor1Geo_CountryCode'])['_id'].nunique().nlargest(
    20).unstack('Actor1Geo_CountryCode').plot.bar()
plt.title('TOP COUNTRIES PER MONTH FOR ACTOR 1')

# 05. TOP FREQUENT COUNTRIES PER MONTH (ACTOR 2)
df.groupby(['MonthYear', 'Actor2Geo_CountryCode'])['_id'].nunique().nlargest(
    20).unstack('Actor2Geo_CountryCode').plot.bar()
plt.title('TOP COUNTRIES PER MONTH FOR ACTOR 2')

# Axis names
plt.ylabel('Number of occurrences')
plt.xlabel('Month')
show()
