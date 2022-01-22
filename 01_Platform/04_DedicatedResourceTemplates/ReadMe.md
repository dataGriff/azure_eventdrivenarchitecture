# Dedicated Resource Deployments

In order for your applications, services and data streaming pipelines to integrare into your new platform, you will need to provide standard templates to make it easy to integrate.

## Publisher

The **[publisher.bicep](publisher.bicep)** code deploys an event hub on to the designated namespace with the parameters you supply and a container for capturing the events that will deploy to the designated storage account. The defaults in the bicep are what I would recommend, including capture being on so that you do not need to worry about losing any historical data. Combined with the lifecyle policies and immutablity already applied in the shared platform deployment, this means that all  data capture, retention and protection has now been handled. These problems have been solved allowing the value to be derived both from streaming data on the hub and guaranteed data capture, all in the same avro format.

Combining this bicep with the key vault powershell deploy in the [DataGriffDeployment.psm1 module](./Modules/DataGriffDeployment.psm1) means that along with the event hub and storage account, the secure keys for the event hub are also available for the application to reference from a key vault immediately in a standard manner. This means the problem of integrating into the skeleton mandatory architecture is easy and value stream teams can focus soley on their local business problem.

The deployment of these publisher assets, the event hub, the storage account container and the key vault with secrets should live with the application, service or data streaming pipeline that is producing this data. There should be a 1:1 coupling between the event producer and these assets, therefore both the code repository reference to the template pipeline (yaml pipeline: TODO) and the deployment of all these assets should live together.

### Quick Start Publisher Demo App

Pre-requisite is you must have deployed the shared infrastructure as per the instructions [here](../02_SharedInfrastructure/ReadMe.md).

To deploy the dedicated app publisher integeation resources of the event hub, the key vault and the storage container into your skeleton platform for a demo application, run the following code in a Powershell terminal, replacing the top three parameters relevant to your environment. This will take a few minutes.

```ps1
$uniqueNamespace = "dgrf"               # Represents the unique id you are applying to your resources to ensure they are globally unique
$subscription = "dataGriff Teaching"    # Name of your azure subscription
$region = "northeurope"                 # Region you are deploying your resources

$eventHubName = "demo"
$deploymentName = "${eventHubName}PublisherDeployment"
$resourceGroupname = "dv-events-broker-rg"
$templateFile = "01_Platform\04_DedicatedResourceTemplates\Bicep\publisher.bicep"
$environment = "dv"
$eventhubnamespaceidentifier = "events001"
$target = "demo"
$sendlisten = 'send'
$teamname = 'demo'

Write-Host "Deploying event hub and storage account..."
New-AzResourceGroupDeployment -name $deploymentName `
    -ResourceGroupName $resourceGroupname `
    -TemplateFile $templateFile `
    -namespace  $uniqueNamespace `
    -eventhubname $eventHubName
Write-Host "Deployed event hub and storage account."

Write-Host "Getting current drive location, assumes in root of azure_deventdrivenarchitecture repo..."
$location = Get-Location
$modulelocation = "$location\01_Platform\04_DedicatedResourceTemplates\Modules\DataGriffDeployment\DataGriffDeployment.psm1"
Write-Host "Attempting to import module from $modulelocation..."
Import-Module -Name $modulelocation
Write-Host "Completed import module from from $modulelocation."

Write-Host "Deploying key vault and event hub secrets..."
    Publish-KeyVaultEventHub -subscription $subscription `
        -environment $environment `
        -uniqueNamespace $uniqueNamespace `
        -region $region `
        -eventhubname $eventhubname `
        -eventhubnamespaceidentifier $eventhubnamespaceidentifier `
        -target $target `
        -sendlisten $sendlisten `
        -teamname $teamname
Write-Host "Deployed key vault and event hub secrets."
```

## Consumer

### Quick Start Demo App Consumer

Pre-requisite is you must have deployed the publisher demo resources as per the instructions [here](###-Quick-Start-Publisher-Demo-App).

To deploy the dedicated app consumer integeation resources of the consumer group and key vault into your skeleton platform for a demo application, run the following code in a Powershell terminal, replacing the top three parameters relevant to your environment. This will take a few minutes.

```ps1
$uniqueNamespace = "dgrf"               # Represents the unique id you are applying to your resources to ensure they are globally unique
$subscription = "dataGriff Teaching"    # Name of your azure subscription
$region = "northeurope"                 # Region you are deploying your resources

$eventHubName = "demo"
$deploymentName = "${eventHubName}PublisherDeployment"
$resourceGroupname = "dv-events-broker-rg"
$templateFile = "01_Platform\04_DedicatedResourceTemplates\Bicep\consumer.bicep"
$environment = "dv"
$eventhubnamespaceidentifier = "events001"
$target = "demo"
$sendlisten = 'listen'
$teamname = 'demo'

Write-Host "Deploying event hub consumer group..."
New-AzResourceGroupDeployment -name $deploymentName `
    -ResourceGroupName $resourceGroupname `
    -TemplateFile $templateFile `
    -namespace  $uniqueNamespace `
    -eventhubname $eventHubName `
    -consumer $target `
    -teamname $teamname
Write-Host "Deployed event hub consumer group."

Write-Host "Getting current drive location, assumes in root of azure_deventdrivenarchitecture repo..."
$location = Get-Location
$modulelocation = "$location\01_Platform\04_DedicatedResourceTemplates\Modules\DataGriffDeployment\DataGriffDeployment.psm1"
Write-Host "Attempting to import module from $modulelocation..."
Import-Module -Name $modulelocation
Write-Host "Completed import module from from $modulelocation."

Write-Host "Deploying key vault and event hub secrets..."
    Publish-KeyVaultEventHub -subscription $subscription `
        -environment $environment `
        -uniqueNamespace $uniqueNamespace `
        -region $region `
        -eventhubname $eventhubname `
        -eventhubnamespaceidentifier $eventhubnamespaceidentifier `
        -target $target `
        -sendlisten $sendlisten `
        -teamname $teamname
Write-Host "Deployed key vault and event hub secrets."
```

# Quick Start Demo Data Stream

## Notes

How to purge a soft delete key vault

```ps1
Remove-AzKeyVault -VaultName "dv-demo-kv-eun-dgrf" -InRemovedState -Location northeurope
```

```bash
az deployment group create --name "publisherDeployment" --resource-group "dv-events-broker-rg" --template-file "01_Platform\04_DedicatedResource\publisher.bicep" --parameters namespace="{youruniqueid}" eventhubname="demo"
```

Need [latest version of powershell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell?view=powershell-7.2) and then
Need to [install-module Az](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-7.0.0) with admin rights for pshell
I had to open up a specific powershell 7 app from my machine
Also restart pshell session in Vs code

```bash
az deployment group create --name "cosmosDeployment" --resource-group "dv-events-account-rg" --template-file "01_Platform\04_DedicatedResource\cosmos.bicep" --parameters namespace="{youruniqueid}" target='account' teamName="customer"
```
