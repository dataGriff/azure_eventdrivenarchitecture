import os
from azure.schemaregistry import SchemaRegistryClient
from azure.schemaregistry.serializer.avroserializer import AvroSerializer
from azure.identity import DefaultAzureCredential, ClientSecretCredential

credential = DefaultAzureCredential()

# token_credential = ClientSecretCredential(
#     tenant_id=TENANT_ID,
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET
# )


fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'
group_name = 'schema_registry'
schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, credential)
serializer = AvroSerializer(client=schema_registry_client, group_name=group_name)

schema_string = """
{"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}"""

with serializer:
    dict_data = {"name": "Ben", "favorite_number": 7, "favorite_color": "red"}
    encoded_bytes = serializer.serialize(dict_data, schema=schema_string)
