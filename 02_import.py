try:
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    import json
    from os.path import dirname, basename, isfile, join    
    from os import listdir
    import glob
except Exception as e:
    print("Some modules are missing")
    
# 01. FIELD NAMES FILE
fieldnames = pd.read_excel('CSV.header.fieldids.xlsx', sheet_name='Sheet1',
                           index_col='Column ID')['Field Name']

#

path = '/Users/Reva/Desktop/DATASET/tmp/MARCH'
files = glob.glob(path + "/*.csv")
print(files)

class MongoDB(object):
    def __init__(self, dbName=None, collectionName=None):
        
        self.dBName = dbName
        self.collectionName = collectionName

        self.client = MongoClient("localhost", 27017)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]

    def InsertData(self):
        dataframe=[]

        for file in files:
            df = pd.read_csv(file, sep='\t', low_memory=False, header=None,
                            dtype=str, names=fieldnames, index_col=['GLOBALEVENTID'])
            dataframe.append(df)
            frame = pd.concat(dataframe, ignore_index=True)
        data = frame.to_dict('records')

        self.collection.insert_many(data)
        print("All the data has been exported to Mongo DB Server")
        print(self.collection.count_documents({}))

if __name__ == "__main__":
    mongodb = MongoDB(dbName='GDELT', collectionName='Events')
    mongodb.InsertData()
    