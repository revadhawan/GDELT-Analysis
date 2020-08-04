# importing frations as parameter values 
from fractions import Fraction as fr
# importing the statistics module 
from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import conda
import os
import scipy.cluster.hierarchy as sch
import seaborn as sb
from matplotlib.pyplot import axis, pie, show
from pymongo import MongoClient
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

os.environ["PROJ_LIB"] = "D:\\Anaconda\Library\share"; #fixr

from mpl_toolkits.basemap import Basemap

# CONNECTION WITH MONGODB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")

db = client.GDELT
coll = db.Events

# FIND EVENTS
# events = coll.find({'MonthYear': '202001'}, no_cursor_timeout=True)
events = coll.aggregate([{'$match': {'ActionGeo_CountryCode': { '$in': ['US','ES','CN','BR','IN','IT','GB','RS','TU','PL'] }}}, {'$sample': { 'size': 2000000 }}], allowDiskUse= True )
data = list(events)
events.close()
df = pd.DataFrame(data)
df = df.replace('null', np.nan, regex=True)
df = df[df['ActionGeo_CountryCode'].notna()]
df = df[df['GoldsteinScale'].notna()]

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

lat_x = pd.to_numeric(df['ActionGeo_Long'], errors='coerce').tolist()
long_y = pd.to_numeric(df['ActionGeo_Lat'], errors='coerce').tolist()

# 01. EVOLUTION OF EVENTS DENSITY
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'])
df.groupby([pd.Grouper(key='SQLDATE',freq='W'),'ActionGeo_CountryCode'])['_id'].nunique().unstack('ActionGeo_CountryCode').plot()
plt.title('Number of events per country')
plt.ylabel('Number of occurrences')
plt.xlabel('Time')
show()

# 02. CLUSTERING
v1 = pd.Categorical(df['ActionGeo_CountryCode']).codes
x = pd.to_numeric(df['EventRootCode']).values
y = pd.to_numeric(df['GoldsteinScale']).values

print(v1, df['ActionGeo_CountryCode'])

fig, ax = plt.subplots(figsize=(8,6))
scatter = ax.scatter(x = x, y = y, c = v1, cmap='tab20b')
legend = ax.legend(*scatter.legend_elements(), loc="lower left", title="Countries" )
ax.add_artist(legend)
plt.ylabel('Goldstein scale')
plt.xlabel('Type of event')
plt.show()


# 03. BASEMAP
goldstein = pd.to_numeric(df['GoldsteinScale']).tolist()
m.scatter(lat_x, long_y, latlon=True, c=goldstein, s=2, cmap='RdYlGn')
bar = m.colorbar()
bar.ax.set_title('Goldstein Scale')
plt.xlabel('Latitude', fontsize=18)
plt.ylabel('Longitude', fontsize=18)
plt.show()

# 04. GS AVERAGE VALUE
mean = [0.65465, -0.187832, 0.940331, 0.752177, 0.511342, 1.117593, 1.052156, 0.569424, 0.533468, 0.669082]
countries = ['US','ES','CN','BR','IN','IT','GB','RS','TU','PL']

plt.rcParams["figure.figsize"] = (8, 8)
fig, ax = plt.subplots()
ax.bar(countries, mean, color="sandybrown")
ax.set(title="Average value for Goldstein Scale")
ax.set(xlabel="Country code", ylabel="Goldstein Scale")

plt.show()