from faker import Faker
import os
import uuid
import datetime
import logging
from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient, PartitionKey
from azure.keyvault.secrets import SecretClient

unique_namespace = os.environ.get('AZURE_UNIQUE_NAMESPACE')
schema_registry_namespace = f"dv-schemaregistry-ehns-eun-{unique_namespace}.servicebus.windows.net"
token_credential =  token_credential = DefaultAzureCredential()
group_name = "myschemagroup"
format = "Avro"
event_hub_name = "demo"
database_name = 'demo'
container_name = 'demo'

KVUri = f"https://dv-demo-kv-eun-{unique_namespace}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
conn_eventhub_publish = client.get_secret("eh-demo-publish").value
conn_cosmos = client.get_secret("cosdb-demo-conn").value

def get_fakedata():
    faker = Faker()
    guid = uuid.uuid4()
    date = datetime.datetime.utcnow()
    email = faker.email()
    print(f'Guid is {guid}')
    print(f'Date is {date}')
    print(f'Email is {email}')

    data = {
        'id': str(guid),
        'date' : str(date),
        'email':  email
    }

    return data

def get_schema():
    schema_string = """{
    "namespace": "example.avro",
    "type": "record",
    "name": "Demo.Created",
    "fields": [
        {
            "name": "id",
            "type": [
                "string"
            ]
        },
        {
            "name": "date",
            "type": [
                "string"
            ]
        },
        {
            "name": "email",
            "type": [
                "string"
            ]
        }
    ]
    }"""
    return schema_string

print('Get schema reg client...')
schema_registry_client = SchemaRegistryClient(schema_registry_namespace, token_credential)
print('Get schema serialiazer...')
avro_serializer = AvroSerializer(client=schema_registry_client, group_name=group_name, auto_register_schemas=True)
print('Get event hub producer client...')
eventhub_producer = EventHubProducerClient.from_connection_string(
    conn_str=conn_eventhub_publish,
    eventhub_name=event_hub_name
)
schema_string = get_schema()

print("Create cosmos client...")
client = CosmosClient.from_connection_string(conn_cosmos)
print("Created cosmos client.")

print("Create database...")
database = client.create_database_if_not_exists(id=database_name)
print("Database created.")

print("Create container...")
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id")
)
print("Container created.")

n = 0
max = 10
if __name__ == '__main__':
    with eventhub_producer, avro_serializer:
        while(n < max):
            data = get_fakedata()
            try:
                container.create_item(body=data)
            except:
                raise ValueError('ERROR: Customer was not created.')
            print('SUCCESS: Demo was created.')
            print(f'Start sending event hub packet {n}')
            event_data_batch = eventhub_producer.create_batch()
            payload_bytes = avro_serializer.serialize(data, schema=schema_string)
            event_data_batch.add(EventData(body=payload_bytes))
            eventhub_producer.send_batch(event_data_batch)
            print(f'Event hub packet {n} sent.')
            n+=1

