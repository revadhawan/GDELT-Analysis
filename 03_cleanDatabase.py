import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient
from matplotlib.pyplot import pie, axis, show

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# 01.CLEANING THE UNWANTED DOCUMENTS
# coll.delete_many({ 'Year': { '$nin': [ '2020'] } })

# 02. CLEANING THE UNWANTED FIELDS
coll.update_many({}, {'$unset': {'FractionDate':1, 
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
                                       'NumSources':1,
                                       'IsRootEvent':1, 
                                       'Actor1Geo_FeatureID':1,
                                       'Actor2Geo_FeatureID':1,
                                       'DATEADDED':1,
                                       'SOURCEURL':1,
                                       'Year':1,
                                       'Actor1KnownGroupCode':1,
                                       'Actor2KnownGroupCode':1,
                                       'Actor1Type1Code':1,
                                       'Actor2Type1Code':1
                                                                              
                                       }})

print('Done')