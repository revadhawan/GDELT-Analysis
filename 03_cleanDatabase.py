import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# 01. Cleaning the unwanted documents
coll.delete_many({ 'Year': { '$nin': [ '2019', '2020'] } })
coll.delete_many({ 'MonthYear': '201909' })

# 02. Cleaning the unwanted fields
""" coll.update_many({}, {'$unset': {'FractionDate':1, 
                                       'Actor1EthnicCode':1,
                                       'Actor1Religion1Code':1,
                                       'Actor1Religion2Code':1,
                                       'Actor1Type2Code':1,
                                       'Actor1Type3Code':1,
                                       'Actor2EthnicCode':1,
                                       'Actor2Religion1Code':1,
                                       'Actor2Religion2Code':1,
                                       'Actor2Type2Code':1,
                                       'Actor2Type3Code':1,
                                       'ActionGeo_FeautreID': 1,
                                       'ActionGeo_ADM1Code': 1,
                                       'Actor1Geo_FeautreID': 1,
                                       'Actor2Geo_FeautreID': 1,
                                       'Actor1Geo_ADM1Code': 1,
                                       'Actor2Geo_ADM1Code': 1,
                                       'NumArticles':1,
                                       'NumSources':1
                                       }}) """

print('Done')