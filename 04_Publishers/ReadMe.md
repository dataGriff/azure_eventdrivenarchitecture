# Create Our Publishers

In this section we are just going to deploy some publishers into our estate in a standard fashion. The first two publishers will use azure functions to publish application events to the common event broker interface, the third will be rows derived from files published to a common event broker interface. This emphasises the fact it is the responsibility of the publishers to make the data available on the common format, regardless of its source data. 

We will be simulating a customer and sales team during this exercise, but also utilising standard deployment pipelines provided by platform, for both publishers and subscribers. Deploying the shared common event broker interface resource upfront allows the platform team to also provide templates for the publisher and consumer pattern on the technology that has been chosen, which is used below. 

**You must have completed [03_SchemaRegistry](..\03_SchemaRegistry\ReadMe.md)before continuing with the below.** 

## Install Python Packages

1. Activate the python environment by running the following.

```py
venv\scripts\activate
```

2. Install the packages required by running the following

```py
pip install faker
pip install azure-eventhub
pip install azure.functions
pip install azure-storage-blob
pip install azure-cosmos
```

### Deploy Event Hub for Publishing Customer Created Event Using the Platform Team Provided Template

We are now going to use the deployment pattern for publishers provided by the platform team in the file [eventhub.bicep](.\platform\eventhub.bicep). This will deploy an event hub and storage account for the customer created event with the following properties:

**Event Hub**
* Data will be retained on the event hub for 7 days.
* Data will be captured every 5 minutes into the accompanyng storage account container.
* 4 Partitions will be added to the event hub which can map to 4 consumer groups. 

**Container**
* The container will be immutable for 7 days so data cannot be removed until after this point.

All of the above properties are configurable in the template parameters.

1. In your Visual Studio code terminal, copy and paste in the following code:

```bash
az deployment group create --name "eventHubDeployment" --resource-group "events-broker-rg" --template-file "04_Publishers\platform\eventhub.bicep" --parameters namespace="{youruniqueid}" event="customer"
```
2. Replace the {youruniqueid} with the uniqueid you have been using for your shared resources and then press return execute.

2. Go into your Azure portal and confirm you can see the "customer" event hub on your events namespace and "customer" container in the events storage account. Confirm that both the event hub and the container have the properties expected from the above. 

**Remember**, this deployment lives with the local customer team, but as the publisher pattern is so common it can utilise a centrally provided platform template for the event publisher objects, that is the event hub and storage container.

1. We're also going to want to have a cosmos db account to store customers that are created, as we can only provide an event in past tense once it has actually occured in the local system. To create the cosmos account, paste the code below into the terminal, again replacing {youruniqueid} with your own unique id.

```bash
az deployment group create --name "cosmosDeployment" --resource-group "events-customer-rg" --template-file "04_Publishers\platform\cosmos.bicep" --parameters namespace="{youruniqueid}" teamName="customer"
```

### Deploy Resources to Start Customer Created Events

This is a timer trigger based function.
Remember the requirements added to txt file which is for all the python packages required.

## Lead Generated

### Deploy Event Hub for Publishing Lead Generated Event Using the Platform Team Provided Template

We're actually going to source the lead generated event from the customer created event, with every customer we get having a chance of being a lead for the sales team. We therefore first need to deploy a new consumer group on the customer event hub for the leads to subscribe from.

1. In your Visual Studio code terminal, copy and paste in the following code:

```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="{youruniqueid}" event="customer" consumer="lead"
```

2. Replace the {youruniqueid} with the uniqueid you have been using for your shared resources and then press return execute.

3. Go to the customer created event hub and look at the consumer groups. You should see "lead" which will represent the dedicated set of data for consumption for leads to be consume. 

Now to deploy the event hub we will publish the leads to...

1. In your Visual Studio code terminal, copy and paste in the following code:

```bash
az deployment group create --name "eventHubDeployment" --resource-group "events-broker-rg" --template-file "04_Publishers\platform\eventhub.bicep" --parameters namespace="{youruniqueid}" event="lead"
```

2. Replace the {youruniqueid} with the uniqueid you have been using for your shared resources and then press return execute.

## Deploy Resources to Generate Lead Generated Event

This is an azure function triggered by an event hub source, in this case the customer created event hub.
Remember to update function.json file
Also update local_settings for your app setting values (e.g. os['setting]) and these need updating in the app settings in portal too.
Also need all packages in the requirements.txt.


## Sale Confirmed

```bash
az deployment group create --name "eventHubDeployment" --resource-group "events-broker-rg" --template-file "04_Publishers\platform\eventhub.bicep" --parameters namespace="griff2" event="sale"
```

```bash
az deployment group create --name "salesFileDeployment" --resource-group "events-salesfiles-rg" --template-file "04_Publishers\lead_purchased\infra\storage.bicep" --parameters namespace="griff2"
```

**Remember to add app setting in portal for function event hub connection!!!**


```
venv\scripts\activate
```

```
04_Publishers\customer_created.py
```

to get functions working remember to install all pre-reqs
also close and reopen vs code when done
add python packages requitred to requitements.txt file (e.g faker)

customer-azfun-eun-griff
lead-azfun-eun-griff
