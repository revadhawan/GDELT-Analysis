import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# Find all events
cursor = coll.aggregate([ {'$match': {"Year": "2020"}}, { '$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)

# Group the events by month
df.groupby('MonthYear')['_id'].nunique().plot(kind='bar')
plt.title('NUMBER OF EVENTS PER MONTH')
plt.ylabel('Number of events')
plt.xlabel('Month')
show()


