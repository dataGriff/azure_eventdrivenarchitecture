$uniqueNamespace = [System.Environment]::GetEnvironmentVariable('AZURE_UNIQUE_NAMESPACE')   # Ensure Resources globally unique
$subscription = [System.Environment]::GetEnvironmentVariable('AZURE_SUBSCRIPTION')          # Name of your azure subscription
$region = [System.Environment]::GetEnvironmentVariable('AZURE_REGION')                      # Region you are deploying your resources

$eventHubName = "demo"
$deploymentName = "${eventHubName}PublisherDeployment"
$resourceGroupname = "dv-events-broker-rg"
$templateFile = "01_Platform\04_DedicatedResourceTemplates\Bicep\consumer.bicep"
$environment = "dv"
$eventhubnamespaceidentifier = "events001"
$target = "demo"
$sendlisten = 'listen'
$teamname = 'demo'

Write-Host "Import module for Powershell deployment..."
Write-Host "Getting current drive location, assumes in root of azure_deventdrivenarchitecture repo..."
$location = Get-Location
$modulelocation = "$location\01_Platform\04_DedicatedResourceTemplates\Modules\DataGriffDeployment\DataGriffDeployment.psm1"
Write-Host "Attempting to import module from $modulelocation..."
Import-Module -Name $modulelocation
Write-Host "Completed import module from from $modulelocation."

Write-Host "Deploying event hub consumer group..."
New-AzResourceGroupDeployment -name $deploymentName `
    -ResourceGroupName $resourceGroupname `
    -TemplateFile $templateFile `
    -namespace  $uniqueNamespace `
    -eventhubname $eventHubName `
    -consumer $target `
    -teamname $teamname
Write-Host "Deployed event hub consumer group."

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