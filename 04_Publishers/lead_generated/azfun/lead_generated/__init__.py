import logging
import azure.functions as func

from azure.eventhub import EventHubProducerClient, EventData
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import ClientSecretCredential

def main(event: func.EventHubEvent):

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
        