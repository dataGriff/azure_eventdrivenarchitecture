import logging
import azure.functions as func
import random
import datetime
import uuid

from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import ClientSecretCredential

def main(event: func.EventHubEvent):

    ## Set Schema Registry Credentials
    fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'
    group_name = "schema_registry"
    tenant_id = "2f9c669b-996b-42d4-8bb2-e94d28032233"
    client_id = "7fd5c6cb-875e-4a63-a02e-0fa55df44884"
    client_secret = "BBv7Q~E33I9DeX9g-hVUBuwiQEKal~vYFrSAt  "
    token_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

    class Customer ():
        def __init__(self, customer_guid, created_date, email):
            self.customer_guid = customer_guid
            self.created_date = created_date
            self.email = email

        def get_customer_details(self):
            logging.info(f"The customer {self.email} has the guid ({self.customer_guid}) and was created on {self.created_date}.")
    
    schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
    avro_serializer = AvroSerializer(client=schema_registry_client
    , group_name=group_name)

    bytes_payload =  event.get_body()

    try:
        deserialized_data = avro_serializer.deserialize(bytes_payload)
        print('The dict data after deserialization is {}'.format(deserialized_data))
        email = deserialized_data.get("email")
        customer_guid = deserialized_data.get("customer_guid")
        created_date = deserialized_data.get("created_date")
        customer = Customer(customer_guid, created_date, email)
        customer.get_customer_details()
    except:
        raise ValueError("This payload is invalid.")

    # generate lead randomly for 1 in 3 customers...
    lead_dice = random.randint(1,3)
    if(lead_dice) == 2:
        logging.info('This customer has taken a lead (the fools!)...')
        fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'

        group_name = "schema_registry"

        ## this is connection to send event hubs to
        eventhub_conn_Str = 'Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=DoiIfBBzWOtUxesDVC70HQSiVTjRAiiIPKEKB8anep4='

        eventhub_producer = EventHubProducerClient.from_connection_string(
            conn_str=eventhub_conn_Str,
            eventhub_name="lead"
        )

        ##this is aprg with permissions on the schema registry that needs to be setup
        tenant_id = "2f9c669b-996b-42d4-8bb2-e94d28032233"
        client_id = "7fd5c6cb-875e-4a63-a02e-0fa55df44884"
        client_secret = "BBv7Q~E33I9DeX9g-hVUBuwiQEKal~vYFrSAt  "
        token_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        schema_string = """
        {"namespace": "example.avro",
        "type": "record",
        "name": "Lead.Generated",
        "fields": [
            {"name": "customer_guid", "type": "string"},
            {"name": "lead_date", "type": "string"},
            {"name": "lead_guid", "type": "string"}
        ]
        }
        """

        data = {
        'customer_guid': str(customer_guid),
        'lead_date' : str(datetime.datetime.utcnow()),
        'lead_guid':  str(uuid.uuid4())
        }

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

    else:
        logging.info('This customer has not taken a lead. More fool them!')
        