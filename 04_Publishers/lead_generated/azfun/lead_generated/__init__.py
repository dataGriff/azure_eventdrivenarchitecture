import logging
import azure.functions as func
import random
import datetime
import uuid
import os

from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import ClientSecretCredential
from azure.cosmos import CosmosClient, PartitionKey

def main(event: func.EventHubEvent):
    class Customer ():
        def __init__(self, id, date, email):
            self.id = id
            self.date = date
            self.email = email

        def get_customer_details(self):
            logging.info(f"The customer {self.email} has the id ({self.id}) and was created on {self.date}.")


    ## Setup Schema Registry Connection Details
    fully_qualified_namespace =  os.environ["schemareg_namespace"]
    source_schema_group = "myschemagroup"
    publish_schema_group = "myschemagroup"
    ##this is aprg with permissions on the schema registry that needs to be setup
    tenant_id = os.environ["tenant_id"]
    schemareg_client_id = os.environ["schemareg_client_id"]
    schemareg_client_secret = os.environ["schemareg_client_secret"]
    token_credential = ClientSecretCredential(tenant_id, schemareg_client_id, schemareg_client_secret)
    ## Set Publisher Connection Details
    conn_eventhub_publish = os.environ["conn_eventhub_publish"]

    ## Connect to Schema Registry
    logging.info('Get schema reg client for source...')
    source_schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
    logging.info('Get schema serialiazer for source...')
    source_avro_serializer = AvroSerializer(client=source_schema_registry_client
    , group_name=source_schema_group)

    ## This event comes from the event hub subcription of the function
    ## Which is listening to customer creation
    source_bytes_payload =  event.get_body()

    ## Attempt to deserialize customer created data
    ## (once we've established we have a new customer we can try to generate a lead)
    try:
        source_deserialized_data = source_avro_serializer.deserialize(source_bytes_payload)
        print('The dict data after deserialization is {}'.format(source_deserialized_data))
        email = source_deserialized_data.get("email")
        customer_id = source_deserialized_data.get("id")
        created_date = source_deserialized_data.get("date")
        customer = Customer(customer_id, created_date, email)
        customer.get_customer_details()
    except:
        raise ValueError("This source payload is invalid.")

    # generate lead randomly for 1 in 3 customers...
    lead_dice = random.randint(1,3)
    if(lead_dice) == 2:
        logging.info('This customer has taken a lead (the fools!)...')

        eventhub_producer = EventHubProducerClient.from_connection_string(
            conn_str=conn_eventhub_publish,
            eventhub_name="lead"
        )

        schema_string = """{
            "namespace": "example.avro",
            "type": "record",
            "name": "Lead.Generated",
            "fields": [
                {
                    "name": "customer_id",
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
                    "name": "lead_date",
                    "type": [
                        "string"
                    ]
                }
            ]
            }"""

        data = {
        'customer_id': str(customer_id),
        'lead_id':  str(uuid.uuid4()),
        'lead_date' : str(datetime.datetime.utcnow()),
        }

        logging.info('Get schema reg client for publish...')
        publish_schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
        logging.info('Get schema serialiazer for publish...')
        publish_avro_serializer = AvroSerializer(client=publish_schema_registry_client, group_name=publish_schema_group, auto_register_schemas=True)

        print("Create cosmos client...")
        endpoint = os.environ["cosmos_endpoint"]
        key = os.environ["cosmos_key"]
        client = CosmosClient(endpoint, key)
        print("Created cosmos client.")

        print("Create database...")
        database_name = 'lead'
        database = client.create_database_if_not_exists(id=database_name)
        print("Database created.")

        print("Create container...")
        container_name = 'lead_generated'
        container = database.create_container_if_not_exists(
            id=container_name, 
            partition_key=PartitionKey(path="/id")
        )
        print("Container created.")


        with eventhub_producer, publish_avro_serializer:
            try:
                container.create_item(body=data)
            except e:
                raise ValueError('ERROR: Lead was not generated.')
            logging.info('SUCCESS: Lead was generated.')
            logging.info('Start sending event hub packet')
            event_data_batch = eventhub_producer.create_batch()
            payload_bytes = publish_avro_serializer.serialize(data, schema=schema_string)
            event_data_batch.add(EventData(body=payload_bytes))
            eventhub_producer.send_batch(event_data_batch)
            logging.info('Event hub packet sent.')

    else:
        logging.info('This customer has not taken a lead. More fool them!')
        