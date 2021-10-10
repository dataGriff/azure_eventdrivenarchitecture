```bash
az login
```

```bash
az account set --subscription "{your subscription name}"
```

```bash
az deployment sub create --name eventResourceGroups --location northeurope --template-file 01_ResourceGroups\main.bicep
```

1. Upload the eventdrivenarchitecture.json dashboard file to your azure portal. 