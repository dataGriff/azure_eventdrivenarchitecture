- [Description](#description)
  - [Architecting the Business Processes & Organisation](#architecting-the-business-processes--organisation)
  - [Architectural Mandate](#architectural-mandate)
    - [Common Schema Standard](#common-schema-standard)
    - [Common Schema Format](#common-schema-format)
  - [Platform Requirements](#platform-requirements)
    - [Cloud First](#cloud-first)
    - [Uniform Interface](#uniform-interface)
    - [Schema Registry](#schema-registry)
    - [Data Compliance](#data-compliance)
    - [Efficient Data Transfer](#efficient-data-transfer)
    - [Clear Resource Ownership](#clear-resource-ownership)
    - [Independent Team Workloads and Deployment](#independent-team-workloads-and-deployment)
    - [Decentralised Security Management](#decentralised-security-management)
  - [Demo](#demo)
    - [Requirements & Dependencies](#requirements--dependencies)
    - [Overview](#overview)
      - [Platform Team](#platform-team)
      - [Product Team](#product-team)
      - [Customer Team](#customer-team)
      - [Conversions Team](#conversions-team)
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

The goal of this repository is to create a complete event driven architecture on azure using appropriate design patterns and strategies. To familiarise with any of the terms of phrases related to event driven architecture, please see the [event driven dictionary](/EventDrivenDictionary.md).

## Architecting the Business Processes & Organisation

The fake organisation used in the demonstration, and how its team setup has been designed around its business function, can be found in the teamconfig solution [here](https://github.com/griff182uk/teamconfig). This is also in development but gives a good bedrock into how you can create an organisation configuration system using programmable Team APIs, informed by event storming and team topologies, influencing the architecture in this demonstration throughout.

## Architectural Mandate

Inspired by the [Jeff Benzos mandate](https://nordicapis.com/the-bezos-api-mandate-amazons-manifesto-for-externalization/) at Amazon, the architecture and organisationisational implementation must adhere to the following rules.

1. Administration overhead must be kept to a minimum with a cloud-first approach and with PaaS or SaaS being preferable.
1. All schemas for business facts should be externalised in a separate registry for ease of discoverability and to prevent coupling on local implementation schemas.  
1. There should be a common data format, common schema standard and uniform interface for all business events to integrate on, with no exception.
1. Data capture, storage and retention should be easily administered to enforce compliance rules easily.
1. Data transfer should be made as quick and easy as possible without the need for complex watermarking.
1. It is the responsibility of all of the event producers to make the data available, explicit with regards to business meaning, and discoverable, with no exception.
1. Each resource should be owned by one team and there should be a one to one relationship betweem a team, a backlog,  a communications channel and a security grouping, establishing clear ownerhship and support networks.
1. Teams can code their owns solutions as long as they integrate on the one common interface across the business and register their outputs in the schema registry.
1. Teams are responsible for ensuring their solutions are production-ready and responsible for any production incidents. "You build it, you run it."
1. Security access for those domain resources that are owned by a team, should be administered by the team.
1. Each team should be able to manage their own workloads and deployment without the need for another team.
1. Any team that does not make its business facts available in a decoupled, explicitly defined with a registered schema on a uniform interface, ~~will be fired~~ will be considered short-sighted and a bad neighbour.

### Common Schema Standard

Without a commn schema format for events produced by the business, there can be no common tooling and the uniform interface integration point of the business will lose its value. [Cloud events](https://cloudevents.io/) appears to be the leading specification in describing events with the [specification](https://github.com/cloudevents/spec/blob/v1.0/spec.md) being adopted by multiple vendors including [Microsoft Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/cloud-event-schema). With the high likelihood of interoperability with other companies required, the architecture mandates that the cloud event [specification](https://github.com/cloudevents/spec/blob/v1.0/spec.md) be adopted for the business.

### Common Schema Format

Avro appears to be the best choice for our event data due to its compatibility with streaming, being a row based optimised data format, it stores metadata with the data and then its ability to support schema evolution. A number of common streaming platforms already use avro as their standard format. Schema evolution is an important factor as it is likely that schemas will change over time, avro is able to keep the data size compact even when multiple schemas exist. Combining this schema evolution capability with externalising the schema in a registry will decouple the publishers and consumers, allowing them to update independently of each other and at their own pace. For more information see this blog post [why you should use avro and schema registry for you streaming applications](https://catherine-shen.medium.com/why-you-should-use-avro-and-schema-registry-for-your-streaming-application-2f24dcf017c8).

## Platform Requirements

### Cloud First

There are a number of cloud vendors on offer, but as the platform team in this instance chose **[Microsoft Azure](https://azure.microsoft.com/en-gb/)**.

### Uniform Interface

A uniform interface is the common data integration point for the entire business. It should be noted that this integration point should become the source of historical as well as real-time data. This integration point is also not simply a queueing mechanism for asyncrhnous processing between one producer and a consumer, but a data store in itself, providing an immutable log of business events.

Azure has two main offerings with respect to this, either to use [Confluent clouds](https://www.confluent.io/) kafka offering, or to use the recently matured **[azure event hub namespaces](https://docs.microsoft.com/en-us/azure/event-hubs/)**, which also have a kafka protocol.

In this demonstration azure event hub namespaces were chosen as the platform as choice because:

- It is a simple low administrative-effort solution.
- It serializes the data as avro as per the architectural requirements.
- Until recently it only had a basic, standard and dedicated offering, but now with the introduction of premium it offers a far more enterprise friendly ready solution. In this workshop the platform will be built using standard, but it is worth noting the [premium](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-premium-overview) capabilities such as up to 100 event hubs on a namespace and the ability to dynamically add partitions for more consumer group. For further comparisons see the [event hub quotas](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas).
- It can handle messages up to 1MB in size which is more than enough for the data requirements of the organisation.
- It now has support for a [schema registry](https://docs.microsoft.com/en-us/azure/event-hubs/create-schema-registry) (even though Confluents is far more mature).
- It automatically [captures data](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview) into blob storage using the capture feature, which can then be leveraged for lifecycle policies (see below) and exposing blob created event grid events to compliment streaming workloads.

### Schema Registry

Even though Confluents schema registry is far more feature rich currently than the Azure schema registry offering, due to the low administrative effort and the fact that event hub namespaces are already being used, the platform team chose to use **[azure schema registry](https://docs.microsoft.com/en-us/azure/event-hubs/schema-registry-overview)**. This schema registry provides backward and forward rules for schema evolution and allows decoupling of operational implementations between publisher and consumer, as well as allowing each consumer to upgrade to different schemas in its own time.

### Data Compliance

 Utilising **[event hub capture](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview)** means that all events published to the event hub are automatically stored in blob storage, as well as living on the event hubs themselves (for up to 90 days in premium). The data being stored in blob means that we can adhere to compliance rules by utilising **[immutability](https://docs.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview)** and **[lifecycle retention policies](https://docs.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview)** to age out data automatically.

### Efficient Data Transfer

In order to adhere to the mandate that efficient data transfer should take place, streaming and event trigger processes are required for the platform. Event hubs already offer a streaming platform which removes the need for complex watermarking code by using independent consumer groups instead. The capture mechanism also cause blob created events to occur which means that event grid triggers can also be utilised if neccessary. Streaming and event driven processes allow for the most efficient and lowest latency data transfer that can be offered. In order to continue to adopt the streaming paradigm into the data lake consumption and analytical tier, **[azure databricks](https://azure.microsoft.com/en-gb/services/databricks/#overview)** has been chosen at the platform to utilise its **[delta file format](https://delta.io/)** that also provides streaming mechanisms of data transfer.

### Clear Resource Ownership

To meet the mandate of clear resource ownership, the platform team can maintain a single list of the team names laid out in the  [teamconfig](https://github.com/griff182uk/teamconfig) example, utilising **[azure policy](https://docs.microsoft.com/en-us/azure/governance/policy/overview)** with a **[tagging strategy](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources?tabs=json)** to ensure resource groups and resources require a team tag and that its value is one of those expected.

### Independent Team Workloads and Deployment

By using **[Azure Devops](https://azure.microsoft.com/en-us/services/devops/)** and setting up an [Azure DevOps project per team](https://docs.microsoft.com/en-us/azure/devops/organizations/projects/about-projects?view=azure-devops), this allows for independent workload management, code administration and deployment by each team independently. Devops security groups per team should also be setup so that they can manage their own projects accordingly. A single group that can read all wikis, work items and all code across the organisation should also be created to ensure knowledge can be shared across teams openly and easily.

### Decentralised Security Management

With Azure being the tooling of choice, **[Azure Active directory](https://azure.microsoft.com/en-gb/services/active-directory/)** will be chosen to manage security. Firstly an azure active directory group should be setup per team described to manage the collections of people more easily. By then utilising a combination of **[PIM](https://docs.microsoft.com/en-us/azure/active-directory/privileged-identity-management/pim-configure)** and potentially **[administrative units](https://docs.microsoft.com/en-us/azure/active-directory/roles/administrative-units)**, the management of the security groups that platform creates with appropriate mapping to each team, can be given to the teams themselves. This decentralizes security management whilst providing a framework from central governance, which must also include suitable auditing and logging to succeed.

## Demo

### Requirements & Dependencies

To see the tooling required and environment setup, including powershell modules, python libraries and how to setup your virtual environment, as well as required windows system environment variables, please see the [prerequisites documentation](Prerequisites.md). Setting this up in advance of you working through the examples will make your life a lot easier.

### Overview

This demo will involve four teams derived from the [teamconfig](https://github.com/griff182uk/teamconfig) setup.
**Important!** This is purely for demonstrative purposes and you should give appropriate time and consideration to your own organisational setup, using appropriate eventstorming, domain design and collaborative effort.

#### Platform Team

- Provide a cloud infrastructure.
- Provide shared infrastructure such as storage accounts and namespaces.
- Provide template deployment pipelines for integrating into shared infrastructure for event producers and event consumers.

#### Product Team

- Configure products resulting in product updated event.

#### Customer Team

- Activates user accounts resulting in account activated event.
- Deactivates user accounts resulting in account deactivated event.
- Activates contact resulting contact activated event.
- Deactivates contact resulting in contact deactivated event.
- Generates a contact who has abandoned a quote resulting in a contact abandoned quote event.
- Updates a contact with purchase details to create a contact purchased event.
- Expires a contract for a contact to generate a contact product expired event.

#### Conversions Team

- Provides users with a product to create lead generated event.
- Fails a user lead to generate a lead failed event.
- Receives sales files to raise a sales file received event.
- Provides sale confirmation to raise a sale confirmed event.

### 1. [Create Platform](/01_Platform)

### 2. [Quick Start](/02_QuickStart)

### 3. [Create Accounts](/03_Accounts)

### 4. [Configure Products](/04_Product)

### 5. [Generate Leads](/05_Leads)

### 6. [Confirm Sales](/06_Sales)

### 7. [Data Pipelines](/07_DataPipelines)

## TODO

- Format schemas as cloud events
- Convert deployments into yaml pipelines.
- Perform same demo using confluent kafka instead of event hubs.
- Possibly change leads into same as sales and take from files so don't do consumers too early.
- Use key vault more, as you are currently not using it :)
- Add tests to confirm all infrastructure in place.
- For the customers that generate leads - it would be good to send the customers who didn't generate a lead to another event hub to represent abandoned leads!
- Need to create local storages for each of the areas as they will have implementation in their local areas. Events are things that have happened but need local storage to happen first really before raising event. e.g. a customer is actually only created once created in a store somewhere.
- Add lifecycle policies to the storage accounts for capture.
- Add and remove lock on resource group deploys.
- Generate lead unsuccesful event?
- Hub per aggregate or event?? Is a customer a purchaser? Who gets in touch with a customer all teams or just crm?

## Foibles

- Have to be owner of schema to delete in registry I think even though this not stated easily. Even when I am god mode.
- When make immutable cannot deploy capture again as keeps trying to override avro file in there.
- Need to sort out dependency of container being deployed before event hub for capture.
- When an event fails once read from a consumer group, how do you handle? Write a checkpoint on error?
- [ASA No Support](https://docs.microsoft.com/en-us/answers/questions/418773/39inputdeserializererrorinvaliddata39-invalid-avro.html) - You can't send schema registered payloads to stream analytics.
- In order to function to read from event hub it needs to use namespace listen. **Security flaw.**
