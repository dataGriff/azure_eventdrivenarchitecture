```
pip install faker
```

```
pip install azure-eventhub
```

Lets make the storage immutable and add/remove a lock on the storage during deploy
so data is bullet proof.
```bash
az deployment group create --name "eventHubDeployment" --resource-group "events-broker-rg" --template-file "04_Publishers\eventhub.bicep" --parameters namespace="griff" event="customer"
```
