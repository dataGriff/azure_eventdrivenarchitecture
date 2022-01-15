Import-Module Az.EventHub

# $subscription = "dataGriff Teaching"
# $environment = "dv"
# $uniqueNamespace = "griff"
# $region = "northeurope"
# $regionshortcode = "eun"
# $eventhubname = "demo"
# $namespaceidentifier = "events001"

# $keyvaultname = "$environment-$eventhubname-kv-$regionshortcode-$uniqueNamespace"
# $resourcegroupname = "$environment-events-account-rg"

# $namespace = "$environment-$namespaceidentifier-ehns-$regionshortcode-$uniqueNamespace"
# $namespaceresourcegroup = "$environment-events-broker-rg"

# $publishsecretname = "eh-$eventhubname-publish"
# $consumesecretname = "eh-$eventhubname-consume"
# $cosmossecretname = "cos-readwrite"

function Connect-Azure
{
    <#
    .SYNOPSIS
    Connects to Azure subscription.

    .DESCRIPTION
    Connects to Azure subscription.

    .PARAMETER SUbscription
    Name of Azure subscription to connect to.

    .EXAMPLE
    $subscription = 'dataGriff Teaching'
    Connect-Azure -subscription $subscription

#>
[CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [String]$subscription
    )
    if ([string]::IsNullOrEmpty($(Get-AzContext).Account))
    {    
        Connect-AzAccount
    }
    Set-AzContext -Subscription $subscription
}

function Get-AzureRegionShortCode
{
    <#
    .SYNOPSIS
    Returns a region shortcode string for region.

    .DESCRIPTION
    Returns a region shortcode string for region.

    .PARAMETER Region
    Name of Azure region.

    .EXAMPLE
    $region = 'northeurope'
    Get-AzureRegionShortCode -region $region

#>
[CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [String]$region
    )

    switch ( $region )
        {
            'northeurope' { $regionshortcode = 'eun'}
            'westeurope' { $regionshortcode = 'euw'}
        }
             
    return $regionshortcode
}

function Publish-KeyVaultEventHub
{
    <#
    .SYNOPSIS
    Publishes connection string to a key vault string for event hub publisher or consumer.

    .DESCRIPTION
    Publishes connection string to a key vault string for event hub publisher or consumer.

    .PARAMETER Subscription
    Name of Azure subscription to connect to.

    .EXAMPLE
    $subscription = "dataGriff Teaching"
    $environment = "dv"
    $uniqueNamespace = "griff"
    $region = "northeurope"
    $eventhubname = "demo"
    $eventhubnamespaceidentifier = "events001"
    $target = "account"
    $sendlisten = 'send'

    Publish-KeyVaultEventHub -subscription $subscription `
        -environment $environment `
        -uniqueNamespace $uniqueNamespace `
        -region $region `
        -eventhubname $eventhubname `
        -eventhubnamespaceidentifier $eventhubnamespaceidentifier `
        -target $target `
        -sendlisten $sendlisten

#>
[CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [String]$subscription,    
        [Parameter(Mandatory = $true)]
        [String]$environment,
        [Parameter(Mandatory = $true)]
        [String]$uniqueNamespace,
        [Parameter(Mandatory = $true)]
        [String]$region,
        [Parameter(Mandatory = $true)]
        [String]$eventhubname,
        [Parameter(Mandatory = $true)]
        [String]$eventhubnamespaceidentifier,
        [Parameter(Mandatory = $true)]
        [String]$target,
        [Parameter(Mandatory = $true)]
        [ValidateSet("send","listen")]
        [String]$sendlisten

    )

    Connect-Azure -subscription $subscription

    $regionshortcode = (Get-AzureRegionShortCode $region)

    $keyvaultname = "$environment-$target-kv-$regionshortcode-$uniqueNamespace"
    Write-Output("Key Vault name is $keyvaultname.")
    $resourcegroupname = "$environment-events-$target-rg"
    Write-Output("Key Vault resource group is $resourcegroupname.")

    $eventhubnamespace = "$environment-$eventhubnamespaceidentifier-ehns-$regionshortcode-$uniqueNamespace"
    Write-Output("Event hub namespace is $eventhubnamespace.")
    $eventhubnamespaceresourcegroup = "$environment-events-broker-rg"
    Write-Output("Event hub namespace resource group is $eventhubnamespaceresourcegroup.")

    if($sendlisten -eq 'send')
    {
        $secretname = "eh-$eventhubname-publish"
        Write-Output("Publish secret name is $secretname.")
    }
    if($sendlisten -eq 'listen')
    {
        $secretname = "eh-$eventhubname-consume"
        Write-Output("Consumer secret name is $secretname.")
    }

    Write-Output("Check if key vault $keyvaultname exists...")
    if(-not(Get-AzKeyVault -VaultName $keyvaultname))
    {
        Write-Output("Key vault $keyvaultname does not exist so deploy...")
        New-AzKeyVault -Name $keyvaultname `
        -ResourceGroupName $resourcegroupname `
        -Location $region
        Write-Output("Key vault $keyvaultname deployed.")
    }
    else {
        Write-Output("Key vault $keyvaultname already exists.")
    }

    Write-Output("Get $sendlisten key for event hub $eventhubname on namespace $eventhubnamespace...")
    $key = (Get-AzEventHubKey -ResourceGroupName $eventhubnamespaceresourcegroup `
        -NamespaceName $eventhubnamespace `
        -EventHubName $eventhubname `
        -AuthorizationRuleName $sendlisten)
    Write-Output("Got $sendlisten key for event hub $eventhubname on namespace $eventhubnamespace.")

    Write-Output("Set key to be secure text...")
    $secretvalue = ConvertTo-SecureString $key.PrimaryConnectionString -AsPlainText -Force
    Write-Output("Set key to be secure text.")

    Write-Output("Add secret $secretname to key vault $keyvaultname...")
    Set-AzKeyVaultSecret -VaultName $keyvaultname `
    -Name $secretname `
    -SecretValue $secretvalue
    Write-Output("Added secret $secretname to key vault $keyvaultname.")

}

$subscription = "dataGriff Teaching"
$environment = "dv"
$uniqueNamespace = "griff"
$region = "northeurope"
$eventhubname = "demo"
$eventhubnamespaceidentifier = "events001"
$target = "account"
$sendlisten = 'listen'

Publish-KeyVaultEventHub -subscription $subscription `
    -environment $environment `
    -uniqueNamespace $uniqueNamespace `
    -region $region `
    -eventhubname $eventhubname `
    -eventhubnamespaceidentifier $eventhubnamespaceidentifier `
    -target $target `
    -sendlisten $sendlisten




## Publish Event Hub Consumer

## Publish Local Cosmos





# $accountName = "dv-customer-cosdb-eun-griff"
# $cosmoskey = (Get-AzCosmosDBAccountKey -ResourceGroupName $resourcegroupname `
#     -Name $accountName -Type "ConnectionStrings")

# $secretvalue = ConvertTo-SecureString $cosmoskey['Secondary SQL Connection String'] -AsPlainText -Force

# Set-AzKeyVaultSecret -VaultName $keyvaultname `
# -Name $cosmossecretname `
# -SecretValue $secretvalue



