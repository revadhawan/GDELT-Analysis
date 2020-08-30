import os

import conda
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from pymongo import MongoClient

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

os.environ["PROJ_LIB"] = "D:\\Anaconda\Library\share"

fig = plt.figure(figsize=(12, 9))

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
db = client.GDELT
coll = db.Events

# FIND ALL EVENTS
events = coll.find(no_cursor_timeout=True)
data = list(events)
events.close()
df = pd.DataFrame(data)

# REMOVE ROWS WITH NAN VALUES
df = df.replace('null', np.nan, regex=True)
df = df[df['ActionGeo_CountryCode'].notna()]
df = df[df['ActionGeo_Long'].notna()]
df = df[df['ActionGeo_Lat'].notna()]

m = Basemap(projection='mill',
            llcrnrlat=-90,
            urcrnrlat=90,
            llcrnrlon=-180,
            urcrnrlon=180,
            resolution='c')

m.drawcoastlines()
m.drawcountries(color='black')

# DEFINE LATITUD AND LONGITUDE VALUES
lat_x = pd.to_numeric(df['ActionGeo_Long'], errors='coerce').tolist()
long_y = pd.to_numeric(df['ActionGeo_Lat'], errors='coerce').tolist()

# 01.GOLDSTEIN SCALE
goldstein = pd.to_numeric(df['GoldsteinScale']).tolist()
m.scatter(lat_x, long_y, latlon=True, c=goldstein, s=2, cmap='RdYlGn')
bar = m.colorbar()
bar.ax.set_title('Goldstein Scale')

# 02. GOLDSTEIN SCALE AVERAGE
df['GoldsteinScale'] = df['GoldsteinScale'].astype(float)
y = list(df.groupby('ActionGeo_CountryCode')['GoldsteinScale'].mean())
m.scatter(lat_x, long_y, latlon=True, c=y, s=2, cmap='RdYlGn')
bar = m.colorbar()
bar.ax.set_title('Goldstein Scale')

# 02. AVERAGE TONE
avgtone = pd.to_numeric(df['AvgTone']).tolist()
m.scatter(lat_x, long_y, latlon=True, c=avgtone,
          s=2, cmap='RdYlGn', vmin=-10, vmax=10)
bar = m.colorbar()
bar.ax.set_title('Average Tone')

# 03. EVENT ROOT CODE
event = pd.to_numeric(df['EventRootCode']).tolist()
m.scatter(lat_x, long_y, latlon=True, c=event, s=2, cmap='RdYlGn')
bar = m.colorbar()
bar.ax.set_title('Event Root Code')

plt.xlabel('Latitude', fontsize=18)
plt.ylabel('Longitude', fontsize=18)
plt.show()
