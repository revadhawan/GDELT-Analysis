import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# Find all events
# cursor = coll.find(no_cursor_timeout=True).limit(1000000)
cursor = coll.aggregate([ {'$match': {"Year": "2020"}}, { '$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)

# Top 10 countries with most events
sums = df.groupby('Actor1CountryCode')['_id'].nunique().nlargest(10)
pie(sums, labels=sums.index)
axis('equal')
plt.title('TOP 10 COUNTRIES FOR ACTOR 1')
plt.ylabel('Number of events')
plt.xlabel('Country code')
show()

# Top 10 countries with most events / month
df.groupby(['MonthYear','Actor1CountryCode'])['_id'].nunique().nlargest(15).unstack('Actor1CountryCode').plot.bar()
plt.title('TOP COUNTRIES PER MONTH FOR ACTOR 1')
plt.ylabel('Number of occurrences')
plt.xlabel('Country code')
show()

#ACTOR 2
# Top 10 countries with most events
sums = df.groupby('Actor2CountryCode')['_id'].nunique().nlargest(10)
pie(sums, labels=sums.index)
axis('equal')
plt.title('TOP 10 COUNTRIES FOR ACTOR 2')
plt.ylabel('Number of events')
plt.xlabel('Country code')
show()

# Top 10 countries with most events / month
df.groupby(['MonthYear','Actor2CountryCode'])['_id'].nunique().nlargest(15).unstack('Actor2CountryCode').plot.bar()
plt.title('TOP COUNTRIES PER MONTH FOR ACTOR 2')
plt.ylabel('Number of occurrences')
plt.xlabel('Country code')
show()