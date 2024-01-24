# flask --debug --app service run

import os
import pickle
import pandas as pd
from pathlib import Path
from azure.storage.blob import BlobServiceClient

# load it again
print(os.environ)

if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
    azureStorageConnectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("try to get containers")
    containers = blob_service_client.list_containers(include_metadata=True)
    print("list containers")
    for container in containers:
        print(container)
        existingContainerName = container['name']
        print(existingContainerName, container['metadata'])
        if existingContainerName.startswith("hikeplanner-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("hikeplanner-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    Path("../model").mkdir(parents=True, exist_ok=True)
    download_file_path = os.path.join("../model", "GradientBoostingRegressor.pkl")
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
         download_file.write(container_client.download_blob(blob.name).readall())


else:
    print("AZURE_STORAGE_CONNECTION_STRING not set")    

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


from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app = Flask(__name__, static_url_path='/', static_folder='../frontend/build')

@app.route("/")
def indexPage():
     return send_file("../frontend/build/index.html")  

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