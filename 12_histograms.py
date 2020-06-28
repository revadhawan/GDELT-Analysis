import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
# events = coll.find(no_cursor_timeout=True).limit(3000000)
events = coll.aggregate([{'$sample': { 'size': 100000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df.columns=df.columns.str.strip()

# GOLDSTEIN SCALE
# 03. NUMBER OF EVENTS IN GOLDSTEIN SCALE
# df.groupby(pd.to_numeric(df['GoldsteinScale']))['_id'].nunique().plot(kind='bar')
# plt.title('NUMBER OF EVENTS IN GOLDSTEIN SCALE')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Goldstein Scale')
# show()

# # 04. EVOLUTION OF NUMBER OF EVENTS IN GOLDSTEIN SCALE
# df.groupby([pd.to_numeric(df['GoldsteinScale']), 'MonthYear'])['_id'].nunique().unstack('MonthYear').plot(kind='bar')
# plt.title('NUMBER OF EVENTS IN GOLDSTEIN SCALE PER MONTH')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Goldstein scale')
# show()

# 05. EVOLUTION OF GOLDSTEIN SCALE AVERAGE
# df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
# df['GoldsteinScale'] = df['GoldsteinScale'].astype(float)
# df.groupby([pd.Grouper(key='SQLDATE',freq='W'),'GoldsteinScale'])['GoldsteinScale'].mean().plot(figsize=(10, 20))
# plt.title('GOLDSTEIN SCALE PER MONTH')
# plt.ylabel('Goldstein scale')
# plt.xlabel('')
# show()

# 05. NUM MENTIONS HISTOGRAM
# df['NumMentions'] = df['NumMentions'].astype(float)
# df['NumMentions'].hist(bins=30, grid=False, figsize=(12,8), color='#39d1ca', range=(0, 50))
# # df['NumMentions'].hist(bins=30, grid=False, figsize=(12,8), color='#39d1ca')
# plt.title('HISTOGRAM OF NUMBER OF MENTIONS')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Number of mentions')
# show()

# 07. HISTOGRAM OF AVERAGE TONE
df['AvgTone'] = df['AvgTone'].astype(float)
df['AvgTone'].hist(bins=15, grid=False, figsize=(12,8), color='#39d1ca', range=(-20, 20))
plt.title('HISTOGRAM OF AVERAGE TONE')
plt.ylabel('Number of occurrences')
plt.xlabel('Average Tone')
show()

# # 07. HISTOGRAM OF GOLDSTEIN SCALE
# df['GoldsteinScale'] = df['GoldsteinScale'].astype(float)
# df['GoldsteinScale'].hist(bins=15, grid=False, figsize=(12,8), color='#39d1ca')
# plt.title('HISTOGRAM OF AVERAGE TONE')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Goldstein Scale')
# show()
