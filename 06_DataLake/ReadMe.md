Data lake is just another subscriber

```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="customer" consumer="datalake"
```

```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="lead" consumer="datalake"
```

```bash
az deployment group create --name "consumerDeployment" --resource-group "events-broker-rg" --template-file "05_Subscribers\platform\consumer.bicep" --parameters namespace="griff2" event="sale" consumer="datalake"
```