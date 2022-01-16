Import-Module Az.EventHub

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
    Write-Host("Start Connect-Azure...")

    if ([string]::IsNullOrEmpty($(Get-AzContext).Account))
    {    
        Connect-AzAccount
    }
    Set-AzContext -Subscription $subscription

    Write-Host("Completed Connect-Azure.")
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

    Write-Host("Start Get-AzureRegionShortCode...")

    switch ( $region )
        {
            'northeurope' { $regionshortcode = 'eun'}
            'westeurope' { $regionshortcode = 'euw'}
        }

    Write-Host("Completed Get-AzureRegionShortCode.")
             
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

    .PARAMETER environment
    The environment code to deploy to which is either dv (development), qa or lv (live).

    .PARAMETER uniqueNamespace
    This is the unique namespace for your azure estate to ensure global uniqueness. e.g. griff.

    .PARAMETER region
    The full name of the azure region. e.g. northeurope.

    .PARAMETER eventhubname
    The name of the event hub you want to retrieve the connection string to publish to or consume from.

    .PARAMETER eventhubnamespaceidentifier
    The name identifier of the event hub namespace. e.g. events001. The namespace name will be constructed as follows:  "$environment-$eventhubnamespaceidentifier-ehns-$regionshortcode-$uniqueNamespace"

    .PARAMETER target
    The name of the area that is wanting to publish to or consume from the event hub. e.g. accout, lead, sale.

    .PARAMETER sendlisten
    Whether the goal is to publish to the event hub ('send') or consume from the event hub ('listen').

    .EXAMPLE
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

#>
[CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [String]$subscription,    
        [Parameter(Mandatory = $true)]
        [ValidateSet("dv","qa","lv")]
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

    Write-Host("Start Publish-KeyVaultEventHub...")

    Connect-Azure -subscription $subscription

    $regionshortcode = (Get-AzureRegionShortCode $region)

    $keyvaultname = "$environment-$target-kv-$regionshortcode-$uniqueNamespace"
    Write-Host("Key Vault name is $keyvaultname.")
    $resourcegroupname = "$environment-events-$target-rg"
    Write-Host("Key Vault resource group is $resourcegroupname.")

    $eventhubnamespace = "$environment-$eventhubnamespaceidentifier-ehns-$regionshortcode-$uniqueNamespace"
    Write-Host("Event hub namespace is $eventhubnamespace.")
    $eventhubnamespaceresourcegroup = "$environment-events-broker-rg"
    Write-Host("Event hub namespace resource group is $eventhubnamespaceresourcegroup.")

    if($sendlisten -eq 'send')
    {
        $secretname = "eh-$eventhubname-publish"
        Write-Host("Publish secret name is $secretname.")
    }
    if($sendlisten -eq 'listen')
    {
        $secretname = "eh-$eventhubname-consume"
        Write-Host("Consumer secret name is $secretname.")
    }

    Write-Host("Check if key vault $keyvaultname exists...")
    if(-not(Get-AzKeyVault -VaultName $keyvaultname))
    {
        Write-Host("Key vault $keyvaultname does not exist so deploy...")
        New-AzKeyVault -Name $keyvaultname `
        -ResourceGroupName $resourcegroupname `
        -Location $region
        Write-Host("Key vault $keyvaultname deployed.")
    }
    else {
        Write-Host("Key vault $keyvaultname already exists.")
    }

    Write-Host("Get $sendlisten key for event hub $eventhubname on namespace $eventhubnamespace...")
    $key = (Get-AzEventHubKey -ResourceGroupName $eventhubnamespaceresourcegroup `
        -NamespaceName $eventhubnamespace `
        -EventHubName $eventhubname `
        -AuthorizationRuleName $sendlisten)
    Write-Host("Got $sendlisten key for event hub $eventhubname on namespace $eventhubnamespace.")

    Write-Host("Set key to be secure text...")
    $secretvalue = ConvertTo-SecureString $key.PrimaryConnectionString -AsPlainText -Force
    Write-Host("Set key to be secure text.")

    Write-Host("Add secret $secretname to key vault $keyvaultname...")
    Set-AzKeyVaultSecret -VaultName $keyvaultname `
    -Name $secretname `
    -SecretValue $secretvalue
    Write-Host("Added secret $secretname to key vault $keyvaultname.")

    Write-Host("Completed Publish-KeyVaultEventHub.")

}

## Publish Local Cosmos





# $accountName = "dv-customer-cosdb-eun-griff"
# $cosmoskey = (Get-AzCosmosDBAccountKey -ResourceGroupName $resourcegroupname `
#     -Name $accountName -Type "ConnectionStrings")

# $secretvalue = ConvertTo-SecureString $cosmoskey['Secondary SQL Connection String'] -AsPlainText -Force

# Set-AzKeyVaultSecret -VaultName $keyvaultname `
# -Name $cosmossecretname `
# -SecretValue $secretvalue



