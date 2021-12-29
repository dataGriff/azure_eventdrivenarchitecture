Import-Module Az.EventHub

$subscription = "dataGriff Teaching"
$environment = "dv"
$uniqueNamespace = "griff"
$region = "northeurope"
$regionshortcode = "eun"
$eventhubname = "demo"
$namespaceidentifier = "events001"

$keyvaultname = "$environment-$eventhubname-kv-$regionshortcode-$uniqueNamespace"
$resourcegroupname = "$environment-events-account-rg"

$namespace = "$environment-$namespaceidentifier-ehns-$regionshortcode-$uniqueNamespace"
$namespaceresourcegroup = "$environment-events-broker-rg"

$publishsecretname = "eh-$eventhubname-publish"
$consumesecretname = "eh-$eventhubname-consume"
$cosmossecretname = "cos-readwrite"

if ([string]::IsNullOrEmpty($(Get-AzContext).Account))
{    
    Connect-AzAccount
}
Set-AzContext -Subscription $subscription

if(Get-AzKeyVault -VaultName $keyvaultname ::IsNullOrEmpty)
{
    New-AzKeyVault -Name $keyvaultname `
    -ResourceGroupName $resourcegroupname `
    -Location $region
}

$sendkey = (Get-AzEventHubKey -ResourceGroupName $namespaceresourcegroup `
-NamespaceName $namespace `
-EventHubName $eventhubname `
-AuthorizationRuleName Send)

$secretvalue = ConvertTo-SecureString $sendkey.PrimaryConnectionString -AsPlainText -Force

Set-AzKeyVaultSecret -VaultName $keyvaultname `
-Name $publishsecretname `
-SecretValue $secretvalue

$listenkey = (Get-AzEventHubKey -ResourceGroupName $namespaceresourcegroup `
-NamespaceName $namespace `
-EventHubName $eventhubname `
-AuthorizationRuleName Listen)

$secretvalue = ConvertTo-SecureString $listenkey.PrimaryConnectionString -AsPlainText -Force

Set-AzKeyVaultSecret -VaultName $keyvaultname `
-Name $consumesecretname `
-SecretValue $secretvalue

$accountName = "dv-customer-cosdb-eun-griff"
$cosmoskey = (Get-AzCosmosDBAccountKey -ResourceGroupName $resourcegroupname `
    -Name $accountName -Type "ConnectionStrings")

$secretvalue = ConvertTo-SecureString $cosmoskey['Secondary SQL Connection String'] -AsPlainText -Force

Set-AzKeyVaultSecret -VaultName $keyvaultname `
-Name $cosmossecretname `
-SecretValue $secretvalue



