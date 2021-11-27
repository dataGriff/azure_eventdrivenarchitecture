## Requirements

* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)
* [Bicep VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)
* [Bicep CLI](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/install#windows)
* [Event Hub VS Code](https://marketplace.visualstudio.com/items?itemName=Summer.azure-event-hub-explorer)


## Demo

This demo will involve three teams:

1. **Platform Team**
* Provide a cloud infrastructure.
* Provide shared infrastructure such as storage accounts and namespaces. 
* Provide template deployment pipelines for integrating into shared infrastructure for event producers and event consumers.

2. **Customer Team**
* Produce Customer Created Event
* Subscribe to Lead Purchased Event
* Produce Customer Purchased Event

1. **Lead Team**
* Produce Lead Generated Event
* Subscribe to Sale Confirmed Event
* Produce Lead Purchased Event

1. **Sales Team**
* Produce Sale Confirmed Event

## 1. Create Resource Groups

[Resource Groups](01_ResourceGroups/ReadMe.md)
## 2. Shared Platform

[Shared Platform](02_SharedPlatform/ReadMe.md)
## 3. Schema 

[SchemaRegistry](03_SchemaRegistry/ReadMe.md)
## 4. Publishers

[Publishers](04_Publishers/ReadMe.md)
## 5. Consumers

## 6. Data Lake

## TODO

* Format schemas as could events
* Convert deployments into yaml pipelines.
* Perform same demo using confluent kafka instead of event hubs.
* Possibly change leads into same as sales and take from files so don't do consumers too early.
* Use key vault more, as you are currently not using it :)
* Add tests to confirm all infrastructure in place. 
* For the customers that generate leads - it would be good to send the customers who didn't generate a lead to another event hub to represent abandoned leads!
* Need to create local storages for each of the areas as they will have implementation in their local areas. Events are things that have happened but need local storage to happen first really before raising event. e.g. a customer is actually only created once created in a store somewhere.
* Add lifecycle policies to the storage accounts for capture.
* Add and remove lock on resource group deploys. 
* Generate lead unsuccesful event?
## Foibles

* Have to be owner of schema to delete in registry I think even though this not stated easily. Even when I am god mode. 
* When make immutable cannot deploy capture again as keeps trying to override avro file in there.
* Need to sort out dependency of container being deployed before event hub for capture.
* When an event fails once read from a consumer group, how do you handle? Write a checkpoint on error? 
* [ASA No Support](https://docs.microsoft.com/en-us/answers/questions/418773/39inputdeserializererrorinvaliddata39-invalid-avro.html) - You can't send schema registered payloads to stream analytics. 
* In order to function to read from event hub it needs to use namespace listen. **Security flaw.**