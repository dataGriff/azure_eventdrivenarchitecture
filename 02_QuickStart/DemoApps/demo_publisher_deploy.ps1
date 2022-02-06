$eventHubName = "demo"
$teamname = 'demo'
$target = "demo"

$uniqueNamespace = [System.Environment]::GetEnvironmentVariable('AZURE_UNIQUE_NAMESPACE')   # Ensure Resources globally unique
$subscription = [System.Environment]::GetEnvironmentVariable('AZURE_SUBSCRIPTION')          # Name of your azure subscription
$region = [System.Environment]::GetEnvironmentVariable('AZURE_REGION')                      # Region you are deploying your resources

$deploymentName = "${eventHubName}PublisherDeployment"
$resourceGroupname = "dv-events-broker-rg"
$templateFile = "01_Platform\05_DedicatedResourceTemplates\Bicep\publisher.bicep"
$environment = "dv"
$eventhubnamespaceidentifier = "events001"
$sendlisten = 'send'

Write-Host "Import module for Powershell deployment..."
Write-Host "Getting current drive location, assumes in root of azure_deventdrivenarchitecture repo..."
$location = Get-Location
$modulelocation = "$location\01_Platform\05_DedicatedResourceTemplates\Modules\DataGriffDeployment\DataGriffDeployment.psm1"
Write-Host "Attempting to import module from $modulelocation..."
Import-Module -Name $modulelocation
Write-Host "Completed import module from from $modulelocation."

Write-Host "Deploying event hub and storage account..."
New-AzResourceGroupDeployment -name $deploymentName `
    -ResourceGroupName $resourceGroupname `
    -TemplateFile $templateFile `
    -namespace  $uniqueNamespace `
    -eventhubname $eventHubName
Write-Host "Deployed event hub and storage account."

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

Write-Host "Deploying cosmos store..."
$deploymentName = "${eventHubName}CosmosDeployment"
$resourceGroupname = "dv-events-demo-rg"
$templateFile = "01_Platform\05_DedicatedResourceTemplates\Bicep\cosmos.bicep"
New-AzResourceGroupDeployment -name $deploymentName `
    -ResourceGroupName $resourceGroupname `
    -TemplateFile $templateFile `
    -namespace  $uniqueNamespace `
    -target $target `
    -teamname $teamname
Write-Host "Deployed cosmos store."

Write-Host "Deploying key vault and cosmos secrets..."
Publish-KeyVaultCosmos -subscription $subscription `
    -environment $environment `
    -uniqueNamespace $uniqueNamespace `
    -region $region `
    -target $target `
    -teamname $teamname
Write-Host "Deployed key vault and cosmos secrets."