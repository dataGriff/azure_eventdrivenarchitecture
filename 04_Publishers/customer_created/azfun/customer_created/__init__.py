import datetime
import logging
import uuid
from faker import Faker

import azure.functions as func
from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import ClientSecretCredential

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    faker = Faker()
    guid = uuid.uuid4()
    date = datetime.datetime.utcnow()
    email = faker.email()
    logging.info(f'Guid is {guid}')
    logging.info(f'Date is {date}')
    logging.info(f'Email is {email}')

    data = {
        'customer_guid': str(guid),
        'created_date' : str(date),
        'email':  email
    }


    fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'

    group_name = "schema_registry"
    format = "Avro"

    ## this is connection to send event hubs to
    eventhub_conn_Str = 'Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=DoiIfBBzWOtUxesDVC70HQSiVTjRAiiIPKEKB8anep4='

    eventhub_producer = EventHubProducerClient.from_connection_string(
        conn_str=eventhub_conn_Str,
        eventhub_name="customer"
    )

    ##this is aprg with permissions on the schema registry that needs to be setup
    tenant_id = "2f9c669b-996b-42d4-8bb2-e94d28032233"
    client_id = "7fd5c6cb-875e-4a63-a02e-0fa55df44884"
    client_secret = "BBv7Q~E33I9DeX9g-hVUBuwiQEKal~vYFrSAt  "
    token_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

    schema_string = """
    {"namespace": "example.avro",
    "type": "record",
    "name": "Customer.Created",
    "fields": [
        {"name": "customer_guid", "type": "string"},
        {"name": "created_date", "type": "string"},
        {"name": "email", "type": "string"}
    ]
    }
    """

    logging.info('Get schema reg client...')
    schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
    logging.info('Get schema serialiazer...')
    avro_serializer = AvroSerializer(client=schema_registry_client, group_name=group_name, auto_register_schemas=True)

    # Schema would be automatically registered into Schema Registry and cached locally.
    logging.info('Get payload...')
    payload = avro_serializer.serialize(data, schema=schema_string)
    logging.info(f'Encoded bytes are: {payload}')

    with eventhub_producer, avro_serializer:
        logging.info('Start sending event hub packet')
        event_data_batch = eventhub_producer.create_batch()
        payload_bytes = avro_serializer.serialize(data, schema=schema_string)
        event_data_batch.add(EventData(body=payload_bytes))
        eventhub_producer.send_batch(event_data_batch)
        logging.info('Event hub packet sent')

    logging.info(f'Python timer trigger function ran at {utc_timestamp}')


