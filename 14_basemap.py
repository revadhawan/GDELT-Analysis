#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import conda
import os

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

from pymongo import MongoClient
from mpl_toolkits.basemap import Basemap


fig = plt.figure(figsize=(12,9))

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
events = coll.aggregate([{'$sample': { 'size': 1000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)

m = Basemap(projection='mill',
            llcrnrlat = -90,
            urcrnrlat = 90,
            llcrnrlon = -180,
            urcrnrlon = 180,
            resolution = 'c') 

m.drawcoastlines()
m.drawcountries(color='black')
# m.drawstates(color='blue')
# m.fillcontinents(color='lightgreen')

lat_x = pd.to_numeric(df['ActionGeo_Long']).tolist()
long_y = pd.to_numeric(df['ActionGeo_Lat']).tolist()


# 01.GOLDSTEIN SCALE
# goldstein = pd.to_numeric(df['GoldsteinScale']).tolist()
# m.scatter(lat_x, long_y, latlon=True, c=goldstein, s=2, cmap='RdYlGn')
# bar = m.colorbar()
# bar.ax.set_title('Goldstein Scale')

# 02. AVERAGE TONE
# avgtone = pd.to_numeric(df['AvgTone']).tolist()
# m.scatter(lat_x, long_y, latlon=True, c=avgtone, s=2, cmap='RdYlGn', vmin=-10, vmax=10)
# bar = m.colorbar()
# bar.ax.set_title('Average Tone')


# 03. EVENT ROOT CODE
event = pd.to_numeric(df['EventRootCode']).tolist()
m.scatter(lat_x, long_y, latlon=True, c=event, s=2, cmap='RdYlGn')
bar = m.colorbar()
bar.ax.set_title('Event Root Code')


# 03. NUMBER OF MENTIONS
# mentions = pd.to_numeric(df['NumMentions']).tolist()
# m.scatter(lat_x, long_y, latlon=True, c=mentions, s=2, cmap='jet')
# bar = m.colorbar()
# bar.ax.set_title('Number of mentions')


plt.xlabel('Latitude', fontsize=18)
plt.ylabel('Longitude', fontsize=18)
plt.show() 