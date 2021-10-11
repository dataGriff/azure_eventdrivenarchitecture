```bash
az login
```

```bash
az account set --subscription "{your subscription name}"
```

```bash
az deployment group create --name "brokerDeployment" --resource-group "events-broker-rg" --template-file "02_SharedPlatform\broker.bicep" --parameters namespace="griff"
```

```bash
az deployment group create --name "brokerDeployment" --resource-group "events-lake-rg" --template-file "02_SharedPlatform\lake.bicep" --parameters namespace="griff"
```

1. Upload the eventdrivenarchitecture.json dashboard file to your azure portal. 