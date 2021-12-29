from azure.identity._credentials.default import DefaultAzureCredential
from schemaregister import *

fully_qualified_namespace = 'schemaregistry-ehns-eun-griff.servicebus.windows.net'

group_name = "myschemagroup"
format = "Avro"

## Initial Schema Version
schema_name = "ForwardCompatibleEvent.Created"
schema01_definition = """
    {
    "namespace": "example.avro",
    "type": "record",
    "name": "ForwardCompatibleEvent.Created",
    "fields": [
        {
            "name": "test_guid",
            "type": [
                "string"
            ]
        },
        {
            "name": "test_date",
            "type": [
                "string"
            ]
        },
        {
            "name": "product_id",
            "type": [
                "string"
            ]
        }
    ]
}
"""

## Adding Optional Fields is Fine As the Publisher
## Is still supportig the original schema that consumers would use
## There is just now an extra one they may not be using yet
schema02_definition = """
{
    "namespace": "example.avro",
    "type": "record",
    "name": "ForwardCompatibleEvent.Created",
    "fields": [
        {
            "name": "test_guid",
            "type": [
                "string"
            ]
        },
        {
            "name": "test_date",
            "type": [
                "string"
            ]
        },
        {
            "name": "product_id",
            "type": [
                "string"
            ]
        },
        {
            "name": "optional_field",
            "type": [
                "string",
                "null"
            ],
            "default": null
        }
    ]
}
"""

### Adding Mandatory Fields is also Fine as Publisher will be putting this
## As part of their payload and subscribers will use when they need to
schema03_definition = """{
    "namespace": "example.avro",
    "type": "record",
    "name": "ForwardCompatibleEvent.Created",
    "fields": [
        {
            "name": "test_guid",
            "type": [
                "string"
            ]
        },
        {
            "name": "test_date",
            "type": [
                "string"
            ]
        },
        {
            "name": "product_id",
            "type": [
                "string"
            ]
        },
        {
            "name": "optional_field",
            "type": [
                "string",
                "null"
            ],
            "default": null
        },
        {
            "name": "mandatory_field",
            "type": [
                "string"
            ]
        }
    ]
}"""

## Removing Field is not fine as Publisher will not be 
## publishing everything the previous schema of the subscriber expects
schema04_definition = """{
    "namespace": "example.avro",
    "type": "record",
    "name": "ForwardCompatibleEvent.Created",
    "fields": [
        {
            "name": "test_guid",
            "type": [
                "string"
            ]
        },
        {
            "name": "test_date",
            "type": [
                "string"
            ]
        },
        {
            "name": "optional_field",
            "type": [
                "string",
                "null"
            ],
            "default": null
        }
    ]
}"""

## Mandatory fields cannot be renamed as equivalent of deleting a mandatory
## Field and subscribers on old schemas cannot handle this
schema05_definition =  """
    {
    "namespace": "example.avro",
    "type": "record",
    "name": "ForwardCompatibleEvent.Created",
    "fields": [
        {
            "name": "test_guid_renamed",
            "type": [
                "string"
            ]
        },
        {
            "name": "test_date",
            "type": [
                "string"
            ]
        },
        {
            "name": "optional_field",
            "type": [
                "string",
                "null"
            ],
            "default": null
        }
    ]
}"""

schemas = [
     schema01_definition,
     schema02_definition,
     schema03_definition,
     schema04_definition,
     schema05_definition
    ]

if __name__ == '__main__':
    token_credential = DefaultAzureCredential()

    schema_registry_client = SchemaRegistryClient(
        fully_qualified_namespace=fully_qualified_namespace, credential=token_credential)
    attempt = 0
    with schema_registry_client:
        for (schema_string) in schemas:
            try:
                attempt+=1
                print(f"Starting attempt {attempt}...")
                schema_id = register_schema(schema_registry_client, group_name
                , schema_name, schema_string, format)
                schema_str = get_schema_by_id(schema_registry_client, schema_id)
                schema_id = get_schema_id(schema_registry_client, group_name
                , schema_name, schema_string, format)
                print(f"Schema attempt {attempt} successfully uploaded as it is compatible.")
            except:
                print(f"Schema attempt {attempt} unable to be uploaded due to incompatibility.")
