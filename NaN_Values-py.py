import pandas as pd
import matplotlib.pyplot as plt
import socket
import errno  

from pymongo import MongoClient

# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
events = coll.find({'MonthYear': '202001'}, no_cursor_timeout=True)
# events = coll.aggregate([{'$match': {'MonthYear': '202001'}},{'$sample': { 'size': 100}}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)


try:
       percent_missing = df.isnull().sum() * 100 / len(df)
       missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
       missing_value_df.sort_values('percent_missing', inplace=True)
       print(missing_value_df)
#        # return True
# except (error_reply, error_perm, error_temp):
#                 return False
except socket.error as error:
       if error.errno == errno.WSAECONNRESET:
           reconnect()
           retry_action()
       else:
           raise