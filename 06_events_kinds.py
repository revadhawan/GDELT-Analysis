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
events = coll.aggregate([{ '$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)


# 01. NUMBER OF EVENTS GROUPED BY THEIR KIND
df.groupby('EventRootCode')['_id'].nunique().plot(kind='bar')
plt.title('TOTAL KIND OF EVENTS')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

# 02. TOP 5 KIND OF EVENTS WITH MOST FREQUENCY
sums = df.groupby('EventRootCode')['_id'].nunique().nlargest(5)
pie(sums, labels=sums.index, autopct='%1.1f%%')
axis('equal')
plt.title('TOP KIND OF EVENTS')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

# 03. NUMBER EVENTS BY THEIR KIND PER MONTH
df.groupby(['MonthYear','EventRootCode'])['_id'].nunique().unstack('MonthYear').plot.bar()
plt.title('KIND OF EVENTS PER MONTH')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

