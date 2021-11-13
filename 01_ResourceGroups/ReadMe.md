# Setup Resource Groups

In this section we will create the resource group shell of our estate using bicep and then create an azure dashboard displaying all the components.
The resource groups would normally be deployed by the respective teams (platform, customer and sales) but doing this for the workshop simply makes the estate easier to navigate from the offset.

**You must have all the pre-requisites completed before carrying out the below.**

1. Open up the azure_eventdrivenarchitecture repo in visual studio code.

2. Open up the Terminal by goig to view > terminal in the visual studio code menu.

3. Ensure that command prompt is chosen in the right of the terminal.

4. Login to Azure running the Azure CLI command below in the terminal.

```bash
az login
```

5. Set the azure subscription you are going to be using by running the command below in the terminal, replacing {your subscription name} with your subscription name.

```bash
az account set --subscription "{your subscription name}"
```

6. Deploy the resource groups for the architecture by running he command below in the terminal.

```bash
az deployment sub create --name eventResourceGroups --location northeurope --template-file 01_ResourceGroups\main.bicep
```

7. To upload your dashboard overview of the architecture, go to the azure portal and choose dashboard from the left menu.

8. Select new dashboard and then upload file.

9. Upload the 01_ResourceGroups\eventdrivenarchitecture.json file.

10. You should now see the empty resource group shell of the entire estate. Confirm you can see the following resource groups and also the team name tags on each one.

* events-schemaregistry-rg (Team: Platform)
* events-customer-rg (Team: Customer)
* events-leads-rg (Team: Sales)
* events-salesfiles-rg (Team: Sales)
* events-sales-rg (Team: Sales)
* events-broker-rg (Team: Platform)
* events-databricks-rg (Team: Platform)
* events-lake-rg (Team: Platform)
