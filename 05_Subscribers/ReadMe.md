```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="customer" consumer="lead"
```

```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="lead" consumer="customer"
```

```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="sale" consumer="customer"
```