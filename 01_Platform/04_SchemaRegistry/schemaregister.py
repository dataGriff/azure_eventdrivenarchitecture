from azure.schemaregistry import SchemaRegistryClient
from azure.identity import DefaultAzureCredential

def register_schema(client, group_name, name, schema_string, format):
    print("Registering schema...")
    schema_properties = client.register_schema(group_name, name, schema_string, format)
    print("Schema registered, returned schema id is {}".format(schema_properties.id))
    print("Schema properties are {}".format(schema_properties))
    return schema_properties.id


def get_schema_by_id(client, id):
    print("Getting schema by id...")
    schema = client.get_schema(id)
    print("The schema string of schema id: {} string is {}".format(id, schema.schema_definition))
    print("Schema properties are {}".format(id))
    return schema.schema_definition


def get_schema_id(client, group_name, name, schema_string, format):
    print("Getting schema id...")
    schema_properties = client.get_schema_properties(group_name, name, schema_string, format)
    print("The schema id is: {}".format(schema_properties.id))
    print("Schema properties are {}".format(schema_properties))
    return schema_properties.id