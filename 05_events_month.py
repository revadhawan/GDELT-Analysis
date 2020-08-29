import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND FILTERED EVENTS
cursor = coll.aggregate([{ '$sample': { 'size': 30 }}], allowDiskUse= True )
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)

df['country_code'] = df['ActionGeo_CountryCode'].values
print(df['country_code'])

# 01. GET EVENTS GROUPED BY MONTH
df.groupby('MonthYear')['_id'].nunique().plot(kind='bar')
plt.title('NUMBER OF EVENTS PER MONTH')
plt.ylabel('Number of events')
plt.xlabel('Month')
show()

# 02. EVOLUTION OF EVENTS DENSITY
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
df.groupby(pd.Grouper(key='SQLDATE',freq='W'))['_id'].nunique().plot()
plt.title('EVOLUTION OF EVENTS DENSITY')
plt.ylabel('Number of events')
plt.xlabel('Month')
show()



