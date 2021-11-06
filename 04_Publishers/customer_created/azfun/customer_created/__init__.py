import datetime
import logging
import uuid
import os
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

    ## Generate Fake Customer Data
    faker = Faker()
    guid = uuid.uuid4()
    date = datetime.datetime.utcnow()
    email = faker.email()
    logging.info(f'Guid is {guid}')
    logging.info(f'Date is {date}')
    logging.info(f'Email is {email}')

    data = {
        'id': str(guid),
        'date' : str(date),
        'email':  email
    }

    ## Setup Schema Registry Connection Details
    fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'
    group_name = "myschemagroup"
    format = "Avro"
    ##this is aprg with permissions on the schema registry that needs to be setup
    tenant_id = os.environ["tenant_id"]
    schemareg_client_id = os.environ["schemareg_client_id"]
    schemareg_client_secret = os.environ["schemareg_client_secret"]
    token_credential = ClientSecretCredential(tenant_id, schemareg_client_id, schemareg_client_secret)
    ## Set Publisher Connection Details
    conn_eventhub_publish = os.environ["conn_eventhub_publish"]

    ## Set Schema
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

    logging.info('Get schema reg client...')
    schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
    logging.info('Get schema serialiazer...')
    avro_serializer = AvroSerializer(client=schema_registry_client, group_name=group_name, auto_register_schemas=True)

    # Schema would be automatically registered into Schema Registry and cached locally.
    logging.info('Get payload...')
    payload = avro_serializer.serialize(data, schema=schema_string)
    logging.info(f'Encoded bytes are: {payload}')

    eventhub_producer = EventHubProducerClient.from_connection_string(
        conn_str=conn_eventhub_publish,
        eventhub_name="customer"
    )

    with eventhub_producer, avro_serializer:
        logging.info('Start sending event hub packet')
        event_data_batch = eventhub_producer.create_batch()
        payload_bytes = avro_serializer.serialize(data, schema=schema_string)
        event_data_batch.add(EventData(body=payload_bytes))
        eventhub_producer.send_batch(event_data_batch)
        logging.info('Event hub packet sent')

    logging.info(f'Python timer trigger function ran at {utc_timestamp}')


