import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
# Erlaubnis auf eigenes Konto geben :-)

try:
    print("Azure Blob Storage Python quickstart sample")

    account_url = "https://mosazhaw.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    exists = False
    containers = blob_service_client.list_containers(include_metadata=True)
    # for container in containers:
    #    print(container['name'], container['metadata'])

    for container in containers:            
        print("\t" + container['name'])
        if "hikeplanner-model" in container['name']:
            print("EXISTIERTT BEREITS!")
            exists = True

    if not exists:
        # Create a unique name for the container
        container_name = str("hikeplanner-model")

        # Create the container
        container_client = blob_service_client.create_container(container_name)

except Exception as ex:
    print('Exception:')
    print(ex)