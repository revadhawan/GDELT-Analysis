import glob
import pandas as pd
import pymongo
from pymongo import MongoClient

# 01. FIELD NAMES FILE (COLUMN NAMES)
fieldnames = pd.read_excel('CSV.header.fieldids.xlsx',
                           sheet_name='Sheet1', index_col='Column ID')['Field Name']

# 02. LOCATE PATH WHERE FILES HAVE BEEN DOWNLOADED
path = '/Users/Reva/Desktop/DATASET02/tmp'
files = glob.glob(path + "/*.csv")
print(files)

# 03. EXPORT THESE FILES TO MONGO DB
class MongoDB(object):
    def __init__(self, dbName=None, collectionName=None):

        self.dBName = dbName
        self.collectionName = collectionName

        self.client = MongoClient("localhost", 27017)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]

    def InsertData(self):
        dataframe = []

        for file in files:
            df = pd.read_csv(file, sep='\t', low_memory=False, header=None,
                             dtype=str, names=fieldnames, index_col=['GLOBALEVENTID'])
            dataframe.append(df)
            frame = pd.concat(dataframe, ignore_index=True)
        data = frame.to_dict('records')

        self.collection.insert_many(data)
        print("All the data has been exported to Mongo DB Server")
        print(self.collection.count_documents({}))


# 04. DATABASE AND COLLECTION NAME WHERE IT IS IMPORTED
if __name__ == "__main__":
    mongodb = MongoDB(dbName='GDELT', collectionName='Events')
    mongodb.InsertData()