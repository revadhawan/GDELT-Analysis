from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# 01. GET TOTAL NUMBER OF DOCUMENTS
number_of_events = coll.count_documents({})
print(number_of_events)

# 02. GET TOTAL NUMBER OF DOCUMENTS FILTERING THEM
# events = coll.find({'MonthYear': '202001'}, no_cursor_timeout=True).limit(2)
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['US','SP','CH','BR','IN','IT','UK','RS','TU','PL'] }}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)

count = df.groupby('ActionGeo_CountryCode')['_id'].count()
x1 = list(df.groupby('ActionGeo_CountryCode').groups.keys())
total=sum(count)
print(total)





for events in df:
   number_of_events = coll.count_documents({})
   print(number_of_events)

# 02. GET LIMITED DOCUMENTS
# all_data = coll.find().limit(2)
# for events in all_data:
#    number_of_events = coll.count_documents({})
#    print(number_of_events)

# # 03. GET THE FIRST EVENT FOUND
# one_event = coll.find_one()
# print(one_event)

# # 4. GET ONLY SOME FIELDS (0 = DON'T, 1 = SHOW)
# for fields in coll.find({}, {"_id":0, "Year":1}):
#    print(fields)

# # 05. GET ONE EVENT BY FILTERING ONE FIELD
# filt_one = coll.find_one({"Year": "2019"})
# print(filt_one)

# # 06. GET ALL EVENTS BY FILTERING ONE FIELD
# filt = coll.find({"Year": "2019"})
# for filt_all in filt:
#     print(filt_all)
    

