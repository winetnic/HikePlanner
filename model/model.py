# new terminal
# cd model
# python model.py

import json
from pymongo import MongoClient
import gpxpy
import pandas as pd

import seaborn as sn
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description='Create Model')
parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
args = parser.parse_args()

mongo_uri = args.uri
mongo_db = "tracks"
mongo_collection = "tracks"

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# fetch a single document
track = collection.find_one(projection={"gpx": 0, "url": 0, "bounds": 0, "name": 0})
values = [track.values() for track in collection.find(projection={"gpx": 0, "url": 0, "bounds": 0, "name": 0})]

# we later use track document's field names to label the columns of the dataframe
df = pd.DataFrame(columns=track.keys(), data=values).set_index("_id")

df['avg_speed'] = df['length_3d']/df['moving_time']
df['difficulty_num'] = df['difficulty'].map(lambda x: int(x[1])).astype('int32')

# drop na values
df.dropna()
df = df[df['avg_speed'] < 2] # an avg of > 2m/s is probably not a hiking activity
df = df[df['min_elevation'] > 0]
df = df[df['length_2d'] < 100000]

corr = df.corr(numeric_only=True)

print(corr)
sn.heatmap(corr, annot=True)
# plt.show()

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

y = df.reset_index()['moving_time']
x = df.reset_index()[['downhill', 'uphill', 'length_3d', 'max_elevation']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

# Baseline Linear Regression
lr = LinearRegression()
lr.fit(x_train, y_train)

y_pred_lr = lr.predict(x_test)
r2 = r2_score(y_test, y_pred_lr)
mse = mean_squared_error(y_test, y_pred_lr)

# Mean Squared Error / R2
print("r2:\t{}\nMSE: \t{}".format(r2, mse))

# GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

gbr = GradientBoostingRegressor(n_estimators=50, random_state=9000)
gbr.fit(x_train, y_train)
y_pred_gbr = gbr.predict(x_test)
r2 = r2_score(y_test, y_pred_gbr)
mse = mean_squared_error(y_test, y_pred_gbr)

print("r2:\t{}\nMSE: \t{}".format(r2, mse))

# distanz: m, time: sec (?)
def din33466(downhill, uphill, distance):
    vertical = downhill / 500.0 + uphill / 300.0
    horizontal = distance / 4.0
    return (min(vertical, horizontal) / 2 + max(vertical, horizontal))*3600

def sac(downhill, uphill, distance):
    return (uphill/400.0 + distance/4.0)*3600

print("*** DEMO ***")
downhill = 300
uphill = 700
length = 10000
max_elevation = 1200
print("Downhill: " + str(downhill))
print("Uphill: " + str(uphill))
print("Length: " + str(length))
demoinput = [[downhill,uphill,length,max_elevation]]
demodf = pd.DataFrame(columns=['downhill', 'uphill', 'length_3d', 'max_elevation'], data=demoinput)
demooutput = gbr.predict(demodf)
time = demooutput[0]

import datetime
print("DIN: " + str(datetime.timedelta(seconds=din33466(uphill, downhill, length/1000))))
print("SAC: " + str(datetime.timedelta(seconds=sac(uphill, downhill, length/1000))))
print("Our Model: " + str(datetime.timedelta(seconds=time)))


# Save To Disk
import pickle
# save the classifier
with open('GradientBoostingRegressor.pkl', 'wb') as fid:
    pickle.dump(gbr, fid)    

# load it again
with open('GradientBoostingRegressor.pkl', 'rb') as fid:
    gbr_loaded = pickle.load(fid)