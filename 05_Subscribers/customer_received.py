from logging import error
from azure.eventhub import EventHubConsumerClient
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential

fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'


group_name = "schema_registry"
format = "Avro"

eventhub_conn_Str = 'Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=DoiIfBBzWOtUxesDVC70HQSiVTjRAiiIPKEKB8anep4='

token_credential = DefaultAzureCredential()

class Customer ():
    def __init__(self, customer_guid, created_date, email):
        self.customer_guid = customer_guid
        self.created_date = created_date
        self.email = email

    def get_customer_details(self):
        print(f"The customer {self.email} has the guid ({self.customer_guid}) and was created on {self.created_date}.")
 
 # RECEIVE
def on_event(partition_context, event):
    print("Received event from partition: {}.".format(partition_context.partition_id))
    bytes_payload = b"".join(b for b in event.body)
    print('The received bytes of the EventData is {}.'.format(bytes_payload))
    
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
    
# CREATE A CONSUMER INSTANCE
eventhub_consumer = EventHubConsumerClient.from_connection_string(
    conn_str=eventhub_conn_Str,
    consumer_group='$Default',
    eventhub_name="customer",
)

# CREATE AN AVRO SERIALIZER INSTANCE
schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)
avro_serializer = AvroSerializer(client=schema_registry_client
, group_name=group_name)
##, auto_register_schemas=True)


# CONSUME
with eventhub_consumer, avro_serializer:
    try:
        eventhub_consumer.receive(on_event=on_event)
        # starting_position="-1",  # "-1" is from the beginning of the partition.
    except KeyboardInterrupt:
        print('Quit')