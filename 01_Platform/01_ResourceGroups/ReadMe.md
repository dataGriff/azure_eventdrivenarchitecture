# Setup Resource Groups

In this section we will create the resource group shell of our estate using bicep and then create an azure dashboard displaying all the components.
The resource groups would normally be deployed by the respective teams (platform, customer, product and sales) but doing this for the workshop simply makes the estate easier to navigate from the offset.

If you ever need to quickly cleanup the entire estate and remove all the resource groups and resource, please use the script and instructions found [here](./cleanup.ps1).

**You must have all the pre-requisites completed before carrying out the below.**

1. Open up the azure_eventdrivenarchitecture repo in visual studio code.

2. Open up the Terminal by going to view > terminal in the visual studio code menu.

3. Ensure that command prompt is chosen in the right of the terminal.

![Terminal Command Prompt](../../Images/TerminalCommandPrompt.PNG)

4. Login to Azure running the Azure CLI command below in the terminal.

```bash
az login
```

5. Set the azure subscription you are going to be using by running the command below in the terminal. The %AZURE_SUBSCRIPTION% will come from the value you have placed in your environment variables as part of the pre-requisites.

```bash
az account set --subscription "%AZURE_SUBSCRIPTION%"
```

6. Deploy the resource groups for the architecture by running he command below in the terminal. The %AZURE_REGION% will come from the value you have placed in your environment variables as part of the pre-requisites.

```bash
az policy assignment create --name 'deny-untagged-resource-groups' --display-name 'Require a tag and its value on resource groups Assignment' --scope "%AZURE_SUBSCRIPTION%" --policy '/providers/Microsoft.Authorization/policyDefinitions/8ce3da23-7156-49e4-b145-24f95f9dcb46' --parameters --tagName='team' -teamValue = ''
```

6. Deploy the resource groups for the architecture by running he command below in the terminal. The %AZURE_REGION% will come from the value you have placed in your environment variables as part of the pre-requisites.

```bash
az deployment sub create --name eventResourceGroups --location "%AZURE_REGION%" --template-file 01_Platform\01_ResourceGroups\resourcegroups.bicep
```

7. To upload your dashboard overview of the architecture, go to the azure portal and choose dashboard from the left menu.

![Dashboard](../../Images/Dashboard.PNG)

8. Select new dashboard and then upload.

![Dashboard](../../Images/DashboardUpload.PNG)

9. Upload the 01_ResourceGroups\dv_eventdrivenarchitecture.json file from this repository.

10. You should now see the empty resource group shell of the entire development (dv) estate. Confirm you can see the following resource groups and also the team name tags on each one.

* dv-events-schemaregistry-rg (team: platform)
* dv-events-broker-rg (team: platform)
* dv-events-databricks-rg (team: platform)
* dv-events-lake-rg (team: platform)
* dv-events-product-rg (team: product)
* dv-events-account-rg (team: customer)
* dv-events-contact-rg (team: customer)
* dv-events-leads-rg (team: conversions)
* dv-events-salesfiles-rg (team: conversions)
* dv-events-sales-rg (team: conversions)

![Dashboard](../../Images/DashboardUploaded.PNG)

To confirm tags, click on a resource group and you should see the team tag at the top of the page.

![Resource Group Tagged](../../Images/ResourceGroupTagged.PNG)

**Note:** You will also see a demo resource group tile that is currently empty. This is used as part of a quickstart demo and will only be short-lived and not part of the overall architecture, but it makes it easier to discover by being on the dashboard. 
