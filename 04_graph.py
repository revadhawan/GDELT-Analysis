import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.Dataset
coll = db.Events

cursor = coll.find({"MonthYear": "202001"}, no_cursor_timeout=True).limit(1000)
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)

# Number of kind of events
# df.groupby('EventRootCode')['_id'].nunique().plot(kind='bar')
# plt.title('Kind of events')
# plt.ylabel('Number of occurrences')
# plt.xlabel('Event code')
# plt.show()

events = df.groupby('EventRootCode')['_id'].nunique().value_counts()
events = events[:5,]
plt.title('Kind of events')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
plt.show()
