from azure.identity._credentials.default import DefaultAzureCredential
from schemaregister import *
import os

unique_namespace = os.environ.get('AZURE_UNIQUE_NAMESPACE')
fully_qualified_namespace = f"dv-schemaregistry-ehns-eun-{unique_namespace}.servicebus.windows.net"

print(f'Schemas to be uploaded to namespace {fully_qualified_namespace}...')

group_name = "myschemagroup"
format = "Avro"

## Initial Schema Version
schema_name = "BackwardCompatibleEvent.Created"
schema01_definition = """
    {
    "namespace": "example.avro",
    "type": "record",
    "name": "BackwardCompatibleEvent.Created",
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

## Adding Optional Fields is Fine as does not need to be populated
## by publisher but consumer can reference it in newer schema
## Note to set optional you need to give a default value of NULL
## As Avro schemas always expect a value
schema02_definition = """
{
    "namespace": "example.avro",
    "type": "record",
    "name": "BackwardCompatibleEvent.Created",
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

### Adding Mandatory Fields is Not Fine as Publisher May Not Be Publishing
### On their Version Of Schema and Consumer will have nothing so error
schema03_definition = """{
    "namespace": "example.avro",
    "type": "record",
    "name": "BackwardCompatibleEvent.Created",
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

## Removing Field is Fine as Publisher will still be publishng
## What Consumer Has Been Getting
schema04_definition = """{
    "namespace": "example.avro",
    "type": "record",
    "name": "BackwardCompatibleEvent.Created",
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

## Can't rename mandatory field as equivalent to adding a new mandatory one
schema05_definition =  """
    {
    "namespace": "example.avro",
    "type": "record",
    "name": "BackwardCompatibleEvent.Created",
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
