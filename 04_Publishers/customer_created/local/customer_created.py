from faker import Faker
import uuid
import datetime
from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential

faker = Faker()

guid = uuid.uuid4()
date = datetime.datetime.utcnow()
email = faker.email()
data = {
        'id': str(guid),
        'date' : str(date),
        'email':  email
    }


fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'

group_name = "myschemagroup"
format = "Avro"

eventhub_conn_Str = 'Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=DoiIfBBzWOtUxesDVC70HQSiVTjRAiiIPKEKB8anep4='

eventhub_producer = EventHubProducerClient.from_connection_string(
    conn_str=eventhub_conn_Str,
    eventhub_name="customer"
)

token_credential = DefaultAzureCredential()

schema_string = """{
    "namespace": "example.avro",
    "type": "record",
    "name": "Customer.Created",
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

schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
avro_serializer = AvroSerializer(client=schema_registry_client, group_name=group_name, auto_register_schemas=True)


# Schema would be automatically registered into Schema Registry and cached locally.
payload = avro_serializer.serialize(data, schema=schema_string)
print('Encoded bytes are: ', payload)

with eventhub_producer, avro_serializer:
    event_data_batch = eventhub_producer.create_batch()
    payload_bytes = avro_serializer.serialize(data, schema=schema_string)
    event_data_batch.add(EventData(body=payload_bytes))
    eventhub_producer.send_batch(event_data_batch)

