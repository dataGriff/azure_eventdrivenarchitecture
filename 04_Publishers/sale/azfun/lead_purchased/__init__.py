import logging

import azure.functions as func
import csv
import codecs
import os
import logging
import datetime
import uuid

import azure.functions as func
from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import ClientSecretCredential
from azure.cosmos import CosmosClient, PartitionKey

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    reader=csv.reader(codecs.iterdecode(myblob,'utf-8'),)
    headers = next(reader)
    data_read = [{h:x for (h,x) in zip(headers,row)} for row in reader]
    logging.info(data_read)
        
    for index in range(len(data_read)):
        lead_id = data_read[index]['lead_id']
        sale_date = data_read[index]['purchase_date']
        guid = uuid.uuid4()
        date = datetime.datetime.utcnow()

        data = {
            'id': str(guid),
            'date' : str(date),
            'lead_id':  str(lead_id),
            'sale_date':  str(sale_date)
        }
        logging.info(data)

    ## Setup Schema Registry Connection Details
    fully_qualified_namespace =  os.environ["schemareg_namespace"]
    group_name = "myschemagroup"
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
    "name": "Sale.Confirmation",
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
            "name": "lead_id",
            "type": [
                "string"
            ]
        },
        {
            "name": "sale_date",
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
        eventhub_name="sale"
    )

    print("Create cosmos client...")
    endpoint = os.environ["cosmos_endpoint"]
    key = os.environ["cosmos_key"]
    client = CosmosClient(endpoint, key)
    print("Created cosmos client.")

    print("Create database...")
    database_name = 'sale'
    database = client.create_database_if_not_exists(id=database_name)
    print("Database created.")

    print("Create container...")
    container_name = 'sale_confirmation'
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id")
    )
    print("Container created.")


    with eventhub_producer, avro_serializer:
        try:
            container.create_item(body=data)
        except:
            raise ValueError('ERROR: Sale was not confirmed.')
        logging.info('SUCCESS: Sale was confirmed.')
        logging.info('Start sending event hub packet')
        event_data_batch = eventhub_producer.create_batch()
        payload_bytes = avro_serializer.serialize(data, schema=schema_string)
        event_data_batch.add(EventData(body=payload_bytes))
        eventhub_producer.send_batch(event_data_batch)
        logging.info('Event hub packet sent.')


