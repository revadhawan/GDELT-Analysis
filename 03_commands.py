from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.Dataset
coll = db.Events

# 1. Get total number of events
number_of_events = coll.count_documents({})
print(number_of_events)

# 2. Get all events (return only 2)
all_data = coll.find().limit(2)
for events in all_data:
   print(events)

# 3. Get the first event found
one_event = coll.find_one()
print(one_event)

# 4. Get only some fields (0 = DON'T, 1 = SHOW)
for fields in coll.find({}, {"_id":0, "Year":1}):
   print(fields)

# 5. Get one event by filtering one field
filt_one = coll.find_one({"Year": "2019"})
print(filt_one)

# 6. Get all events by filtering one field
filt = coll.find({"Year": "2019"})
for filt_all in filt:
    print(filt_all)