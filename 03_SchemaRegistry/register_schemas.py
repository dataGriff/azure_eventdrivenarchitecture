from azure.identity._credentials.default import DefaultAzureCredential
from schemaregister import *

fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'

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

if __name__ == '__main__':
    token_credential = DefaultAzureCredential()

    schema_registry_client = SchemaRegistryClient(
        fully_qualified_namespace=fully_qualified_namespace, credential=token_credential)
    with schema_registry_client:
        for (schema_name,schema_string) in schemas.items():
            schema_id = register_schema(schema_registry_client, group_name
            , schema_name, schema_string, format)
            schema_str = get_schema_by_id(schema_registry_client, schema_id)
            schema_id = get_schema_id(schema_registry_client, group_name
            , schema_name, schema_string, format)
