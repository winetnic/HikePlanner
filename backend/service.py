# flask --debug --app service run

import pickle
import pandas as pd
from pathlib import Path

# load it again
file_path = Path(".", "../model/", "GradientBoostingRegressor.pkl")
with open(file_path, 'rb') as fid:
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


from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def home():
    return "backend"

@app.route("/api/predict")
def hello_world():
    downhill = request.args.get('downhill', default = 0, type = int)
    uphill = request.args.get('uphill', default = 0, type = int)
    length = request.args.get('length', default = 0, type = int)

    demoinput = [[downhill,uphill,length,0]]
    demodf = pd.DataFrame(columns=['downhill', 'uphill', 'length_3d', 'max_elevation'], data=demoinput)
    demooutput = gbr.predict(demodf)
    time = demooutput[0]

    return jsonify({'time': str(datetime.timedelta(seconds=time))})