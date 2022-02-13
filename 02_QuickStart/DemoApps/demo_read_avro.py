from io import BytesIO
import csv, uuid, random, datetime
from operator import attrgetter
from avro.datafile import DataFileReader
from avro.io import DatumReader
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential
import os

##for schema reg
unique_namespace = os.environ.get('AZURE_UNIQUE_NAMESPACE')
schema_registry_namespace = f"dv-schemaregistry-ehns-eun-{unique_namespace}.servicebus.windows.net"
group_name = "myschemagroup"
format = "Avro"
token_credential = DefaultAzureCredential()

##for storage account to read
conn_str = 'DefaultEndpointsProtocol=https;AccountName=dvevents001saeundgrf;AccountKey=rdHo3HtycSuHz46b3MjIJwyIznZcP3X+hfmaVotodzo3HgSJkQ72s1EbWD27d8zMRIsQYVPJidX8g4LzPkl/fw==;EndpointSuffix=core.windows.net'
container_name = 'demop'
container = ContainerClient.from_connection_string(conn_str, container_name=container_name)

blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)

## won't have to search all blobs when trigger off event
## this is just for demo
blob_list = []
for blob in container_client.list_blobs():
    if blob.name.endswith('.avro'):
        blob_list.append(blob)

blob_list.sort(key=attrgetter('creation_time'), reverse=True)

files = len(blob_list)-1
filename = blob_list[files].name ##just get latest file
blob_client = ContainerClient.get_blob_client(container, blob=filename)

schema_registry_client = SchemaRegistryClient(schema_registry_namespace, token_credential)
avro_serializer = AvroSerializer(client=schema_registry_client
, group_name=group_name)

downloader = blob_client.download_blob()
stream = BytesIO()
downloader.download_to_stream(stream) # also tried readinto(stream)

reader = DataFileReader(stream, DatumReader())

for event_data in reader:
    body = (event_data["Body"])
    deserialized_data = avro_serializer.deserialize(body)
    print(deserialized_data)
reader.close()




 