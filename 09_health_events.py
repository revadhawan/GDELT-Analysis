import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND FILTERED EVENTS
events = coll.aggregate([ {'$match': {"Actor1Type1Code": "HLH"}}, { '$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)

# 01. EVOLUTION OF HEALTH EVENTS DENSITY
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
df.groupby(pd.Grouper(key='SQLDATE',freq='W'))['_id'].nunique().plot(figsize=(10, 20))
plt.title('EVOLUTION OF EVENTS RELATED TO HEALTH')
plt.ylabel('Number of occurrences')
plt.xlabel('Weeks')
show()

# 02. COUNTRIES WITH HEALTH EVENTS PER MONTH
df.groupby(['MonthYear','ActionGeo_CountryCode'])['_id'].nunique().nlargest(30).unstack('MonthYear').plot.bar(figsize=(10,30))
plt.title('EVENTS RELATED TO HEALTH PER MONTH AND COUNTRY')
plt.ylabel('Number of occurrences')
plt.xlabel('Country code')
show()

# 03. TOP TYPE OF EVENTS RELATED TO HEALTH
sums = df.groupby('EventRootCode')['_id'].nunique().nlargest(5)
pie(sums, labels=sums.index, autopct='%1.1f%%')
axis('equal')
plt.title('TOP KIND OF EVENTS RELATED TO HEALTH')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

# 04. NUMBER EVENTS BY THEIR KIND PER MONTH RELATED TO HEALTH
df.groupby(['MonthYear','EventRootCode'])['_id'].nunique().unstack('MonthYear').plot.bar()
plt.title('KIND OF EVENTS PER MONTH RELATED TO HEALTH ')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()