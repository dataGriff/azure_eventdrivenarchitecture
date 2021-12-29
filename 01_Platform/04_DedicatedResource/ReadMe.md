```bash
az deployment group create --name "publisherDeployment" --resource-group "dv-events-broker-rg" --template-file "01_Platform\04_DedicatedResource\publisher.bicep" --parameters namespace="{youruniqueid}" eventhubname="demo"
```

Need [latest version of powershell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell?view=powershell-7.2) and then 
Need to [install-module Az](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-7.0.0) with admin rights for pshell
I had to open up a specific powershell 7 app from my machine
Also restart pshell session in Vs code

```bash
az deployment group create --name "cosmosDeployment" --resource-group "dv-events-account-rg" --template-file "01_Platform\04_DedicatedResource\cosmos.bicep" --parameters namespace="{youruniqueid}" teamName="customer"
```