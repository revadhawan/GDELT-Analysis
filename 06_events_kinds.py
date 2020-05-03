import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# Find all events
allevents = coll.find(no_cursor_timeout=True).limit(10)
allevents = coll.aggregate([{ '$sample': { 'size': 1000000 }}], allowDiskUse= True )
alldata = list(allevents)
allevents.close()
alldf = pd.DataFrame(alldata)


# Find by the year wanted
# events = coll.find({"Year": "2020"}, no_cursor_timeout=True).limit(3000000)
events = coll.aggregate([ {'$match': {"Year": "2020"}}, { '$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)


# Number of kind of events
alldf.groupby('EventRootCode')['_id'].nunique().plot(kind='bar')
plt.title('TOTAL KIND OF EVENTS')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

# # Top 5 kind of events
sums = alldf.groupby('EventRootCode')['_id'].nunique().nlargest(5)
pie(sums, labels=sums.index)
axis('equal')
plt.title('TOP KIND OF EVENTS')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

# Number of kind of events / month
df.groupby(['MonthYear','EventRootCode'])['_id'].nunique().unstack('MonthYear').plot.bar()
plt.title('KIND OF EVENTS PER MONTH')
plt.ylabel('Number of occurrences')
plt.xlabel('Event code')
show()

