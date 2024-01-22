
import pickle
import pandas as pd

# load it again
with open('GradientBoostingRegressor.pkl', 'rb') as fid:
    gbr = pickle.load(fid)

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
print("Our Model: " + str(datetime.timedelta(seconds=time)))
