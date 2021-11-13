# Setup Shared Platform

In this section we will be taking the role of the Platform team and deploying all the shared resources for the event driven architecture.

**You must have completed [01_ResourceGroups](../01_ResourceGroups/ReadMe.md) before continuing with the below.**

1. Open up the azure_eventdrivenarchitecture repo in visual studio code.

2. Open up the Terminal by goign to view > terminal in the visual studio code menu.

3. Ensure that command prompt is chosen on the right dropdown menu of the terminal.

4. Login to Azure running the Azure CLI command below in the terminal.

```bash
az login
```

5. Set the azure subscription you are going to be using by running the command below in the terminal, replacing {your subscription name} with your subscription name.

```bash
az account set --subscription "{your subscription name}"
```

6. Deploy the schema registry shared infrastructure by running the following command in the terminal, replacing the namespace parameter {my unique namespace} with a unique name you want to use. This ensures that the resource you are deploying is unique in azure. For example I use "griff" as my unique postfix on Azure resources.
Once deployed confirm you can see the event hub namespace **schemaregistry-ehns-eun-{my unique namespace}** in the portal in the **events-schemaregistry-rg** resource group. You should also the resource is tagged with Team: Platform.

```bash
az deployment group create --name "schemaRegistryDeployment" --resource-group "events-schemaregistry-rg" --template-file "02_SharedPlatform\schemaregistry.bicep" --parameters namespace="{my unique namespace}"
```

**Note** - this schema registry could be a part of the event broker namespace itself, we have just kept it separate for now to show scalability and to highlight it as a key component on the estate.

7. Deploy the event broker shared infrastructure by running the following command in the terminal, replacing the namespace parameter {my unique namespace} with the same unique name you used above.
Once deployed confirm you can see the event hub namespace **events001-ehns-eun-{my unique namespace}** and storage account **events001saeun{my unique namespace}** in the portal in the **events-broker-rg** resource group. You should also the resource is tagged with Team: Platform.

```bash
az deployment group create --name "brokerDeployment" --resource-group "events-broker-rg" --template-file "02_SharedPlatform\broker.bicep" --parameters namespace="{my unique namespace}"
```

8. Deploy the data lake shared infrastructure by running the following command in the terminal, replacing the namespace parameter {my unique namespace} with the same unique name you used above.
Once deployed confirm you can see the data lake storage account **lakesaeun{my unique namespace}** in the portal in the **events-lake-rg** resource group. You should also the resource is tagged with Team: Platform.

```bash
az deployment group create --name "lakeDeployment" --resource-group "events-lake-rg" --template-file "02_SharedPlatform\lake.bicep" --parameters namespace="{my unique namespace}"
```

9. Deploy the data lake shared infrastructure by running the following command in the terminal, replacing the namespace parameter {my unique namespace} with the same unique name you used above.
Once deployed confirm you can see the data lake storage account **events-dbw-eun-{my unique namespace}** in the portal in the **events-databricks-rg** resource group. You should also the resource is tagged with Team: Platform.

```bash
az deployment group create --name "databricksDeployment" --resource-group "events-databricks-rg" --template-file "02_SharedPlatform\databricks.bicep" --parameters namespace="{my unique namespace}"
```

10. You have now played the role of the platform team and deployed all the shared assets for the business value teams to utilize.
