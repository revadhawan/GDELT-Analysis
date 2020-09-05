import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import show
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# Filter events
events = coll.aggregate([{'$match': {'Actor1Code': 'CHN', 'Actor2CountryCode': {
                        '$nin': ['CHN']}}}], allowDiskUse=True)
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['Actor1Code'].notna()]

# 01. EVENTS DENSITY EVOLUTION
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
df.groupby(pd.Grouper(key='SQLDATE', freq='W'))[
    '_id'].nunique().plot(figsize=(10, 20))
plt.title('EVOLUTION OF EVENTS DENSITY WITH CHINA AS ACTOR 1 CODE')
plt.ylabel('Number of occurrences')
plt.xlabel('Date')
show()

# Filter events
events = coll.aggregate(
    [{'$match': {'Actor2CountryCode': {'$nin': ['CHN']}}}], allowDiskUse=True)
data = list(events)
events.close()
df = pd.DataFrame(data)

# Remove rows with NaN values
df = df.replace('null', np.nan, regex=True)
df = df[df['Actor2CountryCode'].notna()]

# 02. CORRELATION BETWEEN COUNTRIES AND OTHER COUNTRIES BY MONTH
df.groupby(['MonthYear', 'Actor2CountryCode'])['_id'].nunique().nlargest(
    30).unstack('Actor2CountryCode').plot(kind='bar')
plt.title('CORRELATION BETWEEN CHINA AND OTHER COUNTRIES')
plt.ylabel('Country code')
plt.xlabel('Number of occurrences')
show()
