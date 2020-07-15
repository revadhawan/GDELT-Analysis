from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

db.coll.aggregate([
{
    # only match documents that have this field
    # you can omit this stage if you don't have missing fieldX
    '$match': {'fieldX': {'$nin': [None]}}  
},
{
    '$group': { '_id': '$fieldX', "doc" : {"$first": "$$ROOT"}}
},
{
    '$replaceRoot': { "newRoot": "$doc"}
}
],
allowDiskUse=True)