from azure.schemaregistry import SchemaRegistryClient
from azure.identity import DefaultAzureCredential

token_credential = DefaultAzureCredential()
# Namespace should be similar to: '<your-eventhub-namespace>.servicebus.windows.net/'
fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'
schema_registry_client = SchemaRegistryClient(fully_qualified_namespace, token_credential)

group_name = "schema_registry"
format = "Avro"

customer_name = "customer_created"
customer_schema_definition = """
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

lead_name = "lead_created"
lead_schema_definition = """
{"namespace": "example.avro",
 "type": "record",
 "name": "Lead.Created",
 "fields": [
     {"name": "lead_guid", "type": "string"},
     {"name": "lead_date", "type": "string"},
     {"name": "customer_guid", "type": "string"},
     {"name": "product_id", "type": "int"}
 ]
}
"""

sale_name = "sale_created"
sale_schema_definition = """
{"namespace": "example.avro",
 "type": "record",
 "name": "Sale.Created",
 "fields": [
     {"name": "sale_guid", "type": "string"},
     {"name": "sale_date", "type": "string"},
     {"name": "lead_guid", "type": "string"}
 ]
}
"""

sale_confirmed_name = "sale_confirmed"
sale_confirmed_schema_definition = """
{"namespace": "example.avro",
 "type": "record",
 "name": "Sale.Confirmed",
 "fields": [
     {"name": "sale_guid", "type": "string"},
     {"name": "sale_date", "type": "string"},
     {"name": "lead_guid", "type": "string"},
     {"name": "customer_guid", "type": "string"},
     {"name": "product_id", "type": "int"}
 ]
}
"""

schemas = {
     customer_name: customer_schema_definition,
    lead_name: lead_schema_definition, 
    sale_confirmed_name: sale_confirmed_schema_definition, 
    sale_name: sale_schema_definition} 

schema_registry_client = SchemaRegistryClient(fully_qualified_namespace=fully_qualified_namespace, credential=token_credential)
with schema_registry_client:
    for k, v in schemas.items():
        print(k, v)
        schema_properties = schema_registry_client.register_schema(group_name, k, v, format)
        id = schema_properties.id