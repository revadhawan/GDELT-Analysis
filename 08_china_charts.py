import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# Find all events
# cursor = coll.find({'Actor1CountryCode': 'CHN'}, no_cursor_timeout=True).limit(10000)
cursor = coll.aggregate([ {'$match': {'Actor1CountryCode': 'CHN'}}, { '$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(cursor)
cursor.close()
df = pd.DataFrame(data)

# Events density evolution
df.groupby('SQLDATE')['_id'].nunique().plot()
show()

