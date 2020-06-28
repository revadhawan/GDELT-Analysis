import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
# cursor = coll.find({'timestamp': {'$gte': 'start', '$lte': 'end'}}, no_cursor_timeout=True)
cursor = coll.aggregate([{ '$sample': { 'size': 100000 }}], allowDiskUse= True )
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)

# ACTOR 1

# 01. TOP 10 FREQUENT COUNTRIES
sums = df.groupby('Actor1CountryCode')['_id'].nunique().nlargest(10)
pie(sums, labels=sums.index, autopct='%1.1f%%')
axis('equal')
plt.title('TOP 10 COUNTRIES FOR ACTOR 1')
plt.ylabel('Number of events')
plt.xlabel('Country code')
show()

# 02. TOP 10 FREQUENT COUNTRIES PER MONTH
df.groupby(['MonthYear','Actor1CountryCode'])['_id'].nunique().nlargest(15).unstack('Actor1CountryCode').plot.bar()
plt.title('TOP COUNTRIES PER MONTH FOR ACTOR 1')
plt.ylabel('Number of occurrences')
plt.xlabel('Country code')
show()

# ACTOR 2

# 03. TOP 10 FREQUENT COUNTRIES
sums = df.groupby('Actor2CountryCode')['_id'].nunique().nlargest(10)
pie(sums, labels=sums.index, autopct='%1.1f%%')
axis('equal')
plt.title('TOP 10 COUNTRIES FOR ACTOR 2')
plt.ylabel('Number of events')
plt.xlabel('Country code')
show()

# 04. TOP 10 FREQUENT COUNTRIES PER MONTH
df.groupby(['MonthYear','Actor2CountryCode'])['_id'].nunique().nlargest(15).unstack('Actor2CountryCode').plot.bar()
plt.title('TOP COUNTRIES PER MONTH FOR ACTOR 2')
plt.ylabel('Number of occurrences')
plt.xlabel('Country code')
show()