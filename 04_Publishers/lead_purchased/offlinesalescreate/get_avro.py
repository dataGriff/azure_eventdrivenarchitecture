from io import BytesIO
import random
from operator import attrgetter
from avro.datafile import DataFileReader
from avro.io import DatumReader
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential

##for schema reg
fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'
group_name = "schema_registry"
format = "Avro"
eventhub_conn_Str = 'Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=DoiIfBBzWOtUxesDVC70HQSiVTjRAiiIPKEKB8anep4='
token_credential = DefaultAzureCredential()

##for storage account to read
conn_str = 'DefaultEndpointsProtocol=https;AccountName=events001saeungriff2;AccountKey=9edptIYkUwq7SVVqwuyz8mPgffjja1mXR7f1L/tWN3wpaI6H0941KcVIGuXGCC1sz9ktappJdn7ai5OLV9G38w==;EndpointSuffix=core.windows.net'
container_name = 'customer'
container = ContainerClient.from_connection_string(conn_str, container_name=container_name)

blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)


blob_list = []
for blob in container_client.list_blobs():
    if blob.name.endswith('.avro'):
        blob_list.append(blob)

blob_list.sort(key=attrgetter('creation_time'), reverse=True)

lead_files = len(blob_list)
rand_leads_file_sold_index = random.randint(0,lead_files)
filename = blob_list[rand_leads_file_sold_index].name ##just get latest for sales
blob_client = ContainerClient.get_blob_client(container, blob=filename)

schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
avro_serializer = AvroSerializer(client=schema_registry_client
, group_name=group_name)

downloader = blob_client.download_blob()
stream = BytesIO()
downloader.download_to_stream(stream) # also tried readinto(stream)

reader = DataFileReader(stream, DatumReader())
for event_data in reader:
    body = (event_data["Body"])
    deserialized_data = avro_serializer.deserialize(body)
    customer_guid = deserialized_data.get("customer_guid")
    print(customer_guid)
reader.close()

 