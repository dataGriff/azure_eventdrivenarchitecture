## The following will remove all policy assignments and policies created as part of this demo.
## You will be prompted with a y/n in the command prompt to confirm you want to proceed.

$subscription = [System.Environment]::GetEnvironmentVariable('AZURE_SUBSCRIPTION') 

$assignments = @(
    'RestrictResourceGroupLocationPolicyAssignment',
    'RestrictResourceLocationPolicyAssignment',
    'TeamTagRequiredResourceGroupPolicyAssignment',
    'TeamTagRequiredResourcePolicyAssignment',
    'TeamTagValueDenyResourceGroupPolicyAssignment',
    'TeamTagValueDenyResourcePolicyAssignment'
)

$policies = @(
    'deny-resource-group-tag-and-values',
    'deny-resource-tag-and-values'
)

$confirmation = Read-Host "Are you Sure You Want To Proceed? (y/n)"
if ($confirmation -eq 'y') {
    Write-Host("Start Connect-Azure...")
    if ([string]::IsNullOrEmpty($(Get-AzContext).Account)) {    
        Connect-AzAccount
    }
    Set-AzContext -Subscription $subscription
    Write-Host("Completed Connect-Azure.")

    write-host ('Start removing assignments...')
    foreach ($assignment in $assignments)
    {
        $assigned = Get-AzPolicyAssignment -Name $assignment -ErrorAction SilentlyContinue -ErrorVariable notPresent
        if($assigned){
            write-host("Removing assignment $assignment...")
            $assigned | Remove-AzPolicyAssignment
            write-host("Removed assignment $assignment.")
        }
        else{
            write-host("Assignment $assignment does not exist. No need to remove.")
        }
    }
    write-host ('Completed removing assignments.')

    write-host ('Start removing policies...')
    foreach ($policy in $policies)
    {
        $pol = Get-AzPolicyDefinition -Name $policy -ErrorAction SilentlyContinue -ErrorVariable notPresent
        if($pol){
            write-host("Removing policy $policy...")
            $pol | Remove-AzPolicyDefinition -Force
            write-host("Removed policy $policy.")
        }
        else{
            write-host("Policy $policy does not exist. No need to remove.")
        }
    }
    write-host ('Completed removing policies.')
}
else {
    write-host('Request to remove polciy assignments and policies cancelled.')
}


