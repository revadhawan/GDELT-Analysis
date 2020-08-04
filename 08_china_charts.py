import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
cursor = coll.aggregate([ {'$match': {'Actor1Code': 'CHN', 'Actor2CountryCode': { '$nin': [ 'CHN'] }}}, { '$sample': { 'size': 5000000 }}], allowDiskUse= True )
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)
print(df.count())

# 01. EVENTS DENSITY EVOLUTION
# df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
# df.groupby(pd.Grouper(key='SQLDATE',freq='W'))['_id'].nunique().plot(figsize=(10, 20))
# plt.title('EVOLUTION OF EVENTS DENSITY WITH CHINA AS ACTOR 1 CODE')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Date')
# show()

# 02. CORRELATION BETWEEN COUNTRIES AND OTHER COUNTRIES BY MONTH
df.groupby(['MonthYear','Actor2CountryCode'])['_id'].nunique().nlargest(30).unstack('Actor2CountryCode').plot(kind='bar')
plt.title('CORRELATION BETWEEN CHINA AND OTHER COUNTRIES')
plt.ylabel('Country code')
plt.xlabel('Number of occurrences') 
show()