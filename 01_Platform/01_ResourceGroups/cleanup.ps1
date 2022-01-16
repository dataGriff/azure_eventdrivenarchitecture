## The following will remove all resource groups and resources created as part of this demo.
## You will be prompted with a y/n in the command prompt to confirm you want to proceed.

$subscription = "datagriff Teaching"
$environment = 'dv'

$resourcegroups = @(
    'events-broker-rg',
    'events-schemaregistry-rg',
    'events-lake-rg',
    'events-databricks-rg',
    'events-account-rg',
    'events-contact-rg',
    'events-product-rg',
    'events-leads-rg',
    'events-salesfiles-rg',
    'events-sales-rg'
)

$confirmation = Read-Host "Are you Sure You Want To Proceed? (y/n)"
if ($confirmation -eq 'y') {
    Write-Host("Start Connect-Azure...")
    if ([string]::IsNullOrEmpty($(Get-AzContext).Account)) {    
        Connect-AzAccount
    }
    Set-AzContext -Subscription $subscription
    Write-Host("Completed Connect-Azure.")

    write-host ('Start removing resource groups...')
    foreach ($resourcegroup in $resourcegroups)
    {
        $envresourcegroup = "$environment-$resourcegroup"
        $rg = Get-AzResourceGroup -Name $envresourcegroup -ErrorVariable notPresent -ErrorAction SilentlyContinue
        if($rg){
            write-host("Removing resource group $envresourcegroup...")
            $rg | Remove-AzResourceGroup -Force
            write-host("Removed resource group $envresourcegroup.")
        }
        else{
            write-host("Resource group $envresourcegroup does not exist. No need to remove.")
        }
    }
    write-host ('Completed removing resource groups.')
}
else {
    write-host('Request to remove resource groups cancelled.')
}


