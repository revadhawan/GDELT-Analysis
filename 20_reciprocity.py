from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# 02. GET TOTAL NUMBER OF DOCUMENTS FILTERING THEM
events = coll.aggregate([{'$match': {'Actor2Geo_CountryCode': { '$in': ['US','SP','CH','BR','IN','IT','UK','RS','TU','PL'] }}}, {'$sample': { 'size': 3000000 }}], allowDiskUse= True )
# events = coll.find(no_cursor_timeout=True)
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)
df = df[df['Actor1Geo_CountryCode'].notna()]
df = df[df['Actor2Geo_CountryCode'].notna()]

# Actor 1
# count = df.groupby('Actor1Geo_CountryCode')['_id'].count()
# total=sum(count)
# x = list(df.groupby('Actor1Geo_CountryCode').groups.keys())
# y = count * 100 / total

# print(y)

# Actor 2
count = df.groupby('Actor2Geo_CountryCode')['_id'].count()
x1 = list(df.groupby('Actor2Geo_CountryCode').groups.keys())
total=sum(count)
y1 = count * 100 / total

print(y1)

# _X = np.arange(len(X))

# plt.bar(x, y, 0.4)
# plt.bar(x1, y1, 0.4)
# # plt.xticks(_X, X) # set labels manually
# plt.xlabel('Country Code')
# plt.ylabel('Percentage')
# plt.show()
