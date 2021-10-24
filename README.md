Event Driven Architecture Dictionary

* **Event** - Immutable business fact stated in the past tense. This could be something new being created or the change in state of something that already exists e.g. *Customer Created* or *Customer Email Updated*. It is important that the event is declared in the past tense during design as consumers of these events expect the event to be a source of immutable truth of something that has definitely happened.
* **Implementation Detail** - Anything prior to the production of a business event is an implementation detail. The technology and complexity, no matter how difficult, are secondary to the target event schema that needs to be produced. This means that there is loong-term decoupling from any subscriber to the event and therefore any technology, in particular storage and local schemas, being used by the producer. 
* **Common Interface** - An Event driven architecture aims to provide a common interface for all applications and data pipelines to publish and subscribe to. This is provided by an event broker. This common interface solves a lot of local specialized implementations to provide data between business areas. 
* **Data Products** - Much like the way that applications and websites are treated as products, the production of the data as events should also be treated as products and evolve incrementally to customer requirements just like any other product.
* **Product Owner** - Product owners are needed for the events that are produced in an event driven architecture to ensure they continue to meet business needs.
* **Team Ownership** - It is extremely important that individual events are owned within single long-lived teams. The team will take the responsibility of producing and adhering to the business agreed schema as well as communicating to subscribers when there are any breaking changes. The events themselves should be treated as products produced by the team and be a part of the teams product owner remit. 
* Producer
* Consumer
* Event Broker
* Event Broker Log
* Partition
* Schema Registry
* Topic 
* **Event Storming** - This is the collaborative design of discovering events within and across business domains. This design process should involve all domain experts, business and technical, to derive a common model of the processes and a common language. Event storming is particularly important to get a business-wide view of the events as it can influence schema design to ensure data communication pathways remain robust even with consumer agnostic approachs to event publication by the producer. 
* **Streaming** - Streaming is the idea that data in an event driven architecture there is constantly "data-in-motion" as opposed to "data-at-rest". Applications and data pipelines are able to receive data from a dedicated consumer group without the need for watermarking as the event broker will guarantee at least once delivery and push data to its destination.
* **Immutable Log** - Log not a queue. 



## Requirements

* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)
* [Bicep VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)
* [Bicep CLI](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/install#windows)
* [Event Hub VS Code](https://marketplace.visualstudio.com/items?itemName=Summer.azure-event-hub-explorer)

## Links

* [Bicep](https://learn.hashicorp.com/collections/terraform/azure-get-started)
* [Azure Terraform](https://learn.hashicorp.com/collections/terraform/azure-get-started)
* [Databricks Bicep](https://towardsdatascience.com/creating-azure-databricks-with-bicep-and-azure-devops-yaml-pipelines-4bf85be30cc7)
* [Dynamically Add Partitions in Premium or Dedicated](https://docs.microsoft.com/en-us/azure/event-hubs/dynamically-add-partitions)
* [Python Integration](https://azuresdkdocs.blob.core.windows.net/$web/python/azure-schemaregistry-avroserializer/latest/index.html#event-hubs-sending-integration)
* [Schema Reg Compare](https://www.syntio.net/en/labs-musings/schema-registry-comparison)
* [Schema Registry Spark](https://www.rakirahman.me/azure-schemaregistry-spark/)
* [Event Hub Spark](https://github.com/Azure/azure-event-hubs-spark)
* [Create Function Python](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
* [Install Azure Function Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v3%2Cwindows%2Ccsharp%2Cportal%2Cbash%2Ckeda#install-the-azure-functions-core-tools)
* [Azure Functions VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
* [Python Schema Registry](https://pypi.org/project/azure-schemaregistry-avroserializer/)


## Demo

This demo will involve three teams:
1. Platform Team 
* Provide a cloud infrastructure.
* Provide shared infrastructure such as storage accounts and namespaces. 
* Provide template deployment pipelines for integrating into shared infrastructure for event producers and event consumers.
2. Customer Team
* Produce Customer Created Event
* Subscribe to Lead Generated Event
* Subscribe to Lead Sold Event
* Produce Customer Sale Confirmation Sent Event
3. Sales Team
* Produce Lead Generated Event
* Produce Lead Sold Event

## 1. Create Resource Groups

## 2. Shared Infrastructure
## 3. Schema Registry

## 4. Publishers
## 5. Consumers

## 6. Data Lake

## TODO

* Convert deployments into yaml pipelines.
* Perform same demo using confluent kafka instead of event hubs.
* Possibly change leads into same as sales and take from files so don't do consumers too early.
* Use key vault more, as you are currently not using it :)
## Foibles

* Have to be owner of schema to delete in registry I think even though this not stated easily. Even when I am god mode. 
* When make immutable cannot deploy capture again as keeps trying to override avro file in there.
* Need to sort out dependency of container being deployed before event hub for capture.
* When an event fails once read from a consumer group, how do you handle? Write a checkpoint on error? 