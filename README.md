- [Description](#description)
  - [Requirements & Dependencies](#requirements--dependencies)
  - [Event Driven Dictionary](#event-driven-dictionary)
  - [Demo](#demo)
  - [1. Create Platform](#1-create-platform)
  - [2. Quick Start](#2-quick-start)
  - [3. Create Accounts](#3-create-accounts)
  - [4. Configure Products](#4-configure-products)
  - [5. Generate Leads](#5-generate-leads)
  - [6. Confirm Sales](#6-confirm-sales)
  - [7. Data Pipelines](#7-data-pipelines)
  - [TODO](#todo)
  - [Foibles](#foibles)

# Description

The goal of this repository is to create a complete event driven architecture on azure using appropriate design patterns and strategies.

The fake organisation used in the demonstration, and how its team setup has been designed around its business function, can be found in the teamconfig solution [here](https://github.com/griff182uk/teamconfig). This is also in development but gives a good bedrock into how you can create an organisation configuration system using programmable Team APIs, informed by event storming and team topologies, influencing the architecture in this demonstration throughout.

## Requirements & Dependencies

To see the tooling required and environment setup, including powershell modules, python libraries and how to setup your virtual environment, as well as required windows system environment variables, please see the [prerequisites documentation](Prerequisites.md). Setting this up in advance of you working through the examples will make your life a lot easier.

## Event Driven Dictionary

It would also be a good idea for you to familiarise yourself with some of the terms and patterns found in the [event driven dictionary](/EventDrivenDictionary.md).

## Demo

This demo will involve four teams:

1. **Platform Team**
* Provide a cloud infrastructure.
* Provide shared infrastructure such as storage accounts and namespaces. 
* Provide template deployment pipelines for integrating into shared infrastructure for event producers and event consumers.

2. **Product Team**
* Produce Customer Created Event
* Subscribe to Lead Purchased Event
* Produce Customer Purchased Event

2. **Customer Team**
* Produce Customer Created Event
* Subscribe to Lead Purchased Event
* Produce Customer Purchased Event

1. **Conversions Team**
* Produce Lead Generated Event
* Subscribe to Sale Confirmed Event
* Produce Lead Purchased Event
* Produce Sale Confirmed Event

## 1. [Create Platform](/01_Platform)

## 2. [Quick Start](/02_QuickStart)

## 3. [Create Accounts](/03_Accounts)

## 4. [Configure Products](/04_Product)

## 5. [Generate Leads](/05_Leads)

## 6. [Confirm Sales](/06_Sales)

## 7. [Data Pipelines](/07_DataPipelines)

## TODO

* Format schemas as cloud events
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
* Hub per aggregate or event?? Is a customer a purchaser? Who gets in touch with a customer all teams or just crm? 
## Foibles

* Have to be owner of schema to delete in registry I think even though this not stated easily. Even when I am god mode. 
* When make immutable cannot deploy capture again as keeps trying to override avro file in there.
* Need to sort out dependency of container being deployed before event hub for capture.
* When an event fails once read from a consumer group, how do you handle? Write a checkpoint on error? 
* [ASA No Support](https://docs.microsoft.com/en-us/answers/questions/418773/39inputdeserializererrorinvaliddata39-invalid-avro.html) - You can't send schema registered payloads to stream analytics. 
* In order to function to read from event hub it needs to use namespace listen. **Security flaw.**