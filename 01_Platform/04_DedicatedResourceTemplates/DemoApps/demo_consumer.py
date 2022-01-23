from logging import error
import os
from azure.eventhub import EventHubConsumerClient
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

unique_namespace = os.environ.get('AZURE_UNIQUE_NAMESPACE')
schema_registry_namespace = f"dv-schemaregistry-ehns-eun-{unique_namespace}.servicebus.windows.net"
token_credential =  token_credential = DefaultAzureCredential()
group_name = "myschemagroup"
format = "Avro"
event_hub_name = "demo"
consumer_group_name = "demo"

KVUri = f"https://dv-demo-kv-eun-{unique_namespace}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
conn_eventhub_consume = client.get_secret("eh-demo-consume").value

token_credential = DefaultAzureCredential()

class Customer ():
    def __init__(self, id, date, email):
        self.id = id
        self.date = date
        self.email = email

    def get_customer_details(self):
        print(f"The customer {self.email} has the id {self.id} and was created on {self.date}.")
 
 # RECEIVE
def on_event(partition_context, event):
    print("Received event from partition: {}.".format(partition_context.partition_id))
    bytes_payload = b"".join(b for b in event.body)
    print('The received bytes of the EventData is {}.'.format(bytes_payload))
    
    try:
        deserialized_data = avro_serializer.deserialize(bytes_payload)
        print('The dict data after deserialization is {}'.format(deserialized_data))
        email = deserialized_data.get("email")
        customer_guid = deserialized_data.get("id")
        created_date = deserialized_data.get("date")
        customer = Customer(customer_guid, created_date, email)
        customer.get_customer_details()
    except:
        raise ValueError("This payload is invalid.")

    
# CREATE A CONSUMER INSTANCE
eventhub_consumer = EventHubConsumerClient.from_connection_string(
    conn_str=conn_eventhub_consume,
    consumer_group=consumer_group_name,
    eventhub_name=event_hub_name,
)

# CREATE AN AVRO SERIALIZER INSTANCE
schema_registry_client = SchemaRegistryClient(schema_registry_namespace, token_credential)
avro_serializer = AvroSerializer(client=schema_registry_client
, group_name=group_name)

# CONSUME
if __name__ == '__main__':
    with eventhub_consumer, avro_serializer:
        try:
            print('Receive events...')
            eventhub_consumer.receive(on_event=on_event)
            # starting_position="-1",  # "-1" is from the beginning of the partition.
        except KeyboardInterrupt:
            print('Quit')
