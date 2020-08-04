import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
events = coll.aggregate([{ '$sample': { 'size': 100000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

# QUAD CLASS
# 01. QUAD CLASSES DENSITY
# sums = df.groupby('QuadClass')['_id'].nunique()
# pie(sums, labels=sums.index, autopct='%1.1f%%')
# axis('equal')
# plt.title('DENSITY OF EVENTS GROUPED BY QUAD CLASS')
# plt.ylabel('Percentage of occurrences')
# plt.xlabel('Quad class')
# show()

# 02. EVOLUTION OF QUAD CLASSES DENSITY
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
df.groupby(['QuadClass', pd.Grouper(key='SQLDATE',freq='W')])['_id'].nunique().unstack('QuadClass').plot()
plt.title('EVOLUTION OF QUAD CLASSES DENSITY')
plt.ylabel('Number of occurrences')
plt.xlabel('Quad class')
show()

# GOLDSTEIN SCALE
# 03. NUMBER OF EVENTS IN GOLDSTEIN SCALE
# df.sort_values(pd.to_numeric(df['GoldsteinScale']), ascending=True).groupby(pd.to_numeric(df['GoldsteinScale']))['_id'].nunique().nlargest(20).plot.bar()
# plt.title('NUMBER OF EVENTS IN GOLDSTEIN SCALE')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Goldstein scale')
# show()

# 04. EVOLUTION OF NUMBER OF EVENTS IN GOLDSTEIN SCALE
# df.groupby([pd.to_numeric(df['GoldsteinScale']), 'MonthYear'])['_id'].nunique().unstack('MonthYear').plot()
# plt.title('GOLDSTEIN SCALE PER MONTH')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Goldstein scale')
# show()