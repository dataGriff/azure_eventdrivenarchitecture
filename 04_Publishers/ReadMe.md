```
pip install faker
```

```
pip install azure-eventhub
```

```
pip install azure.functions
```

```
pip install azure-storage-blob
```

Lets make the storage immutable and add/remove a lock on the storage during deploy
so data is bullet proof.
```bash
az deployment group create --name "eventHubDeployment" --resource-group "events-broker-rg" --template-file "04_Publishers\platform\eventhub.bicep" --parameters namespace="griff2" event="customer"
```

This is subscriber but needed as we're using it to regenerate leads with consistent lead guid
```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="customer" consumer="lead"
```

```bash
az deployment group create --name "eventHubDeployment" --resource-group "events-broker-rg" --template-file "04_Publishers\platform\eventhub.bicep" --parameters namespace="griff2" event="lead"
```

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
