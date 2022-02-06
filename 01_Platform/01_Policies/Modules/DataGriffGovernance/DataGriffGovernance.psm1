function Connect-Azure {
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

    if ([string]::IsNullOrEmpty($(Get-AzContext).Account)) {    
        Connect-AzAccount
    }
    Set-AzContext -Subscription $subscription

    Write-Host("Completed Connect-Azure.")
}

function Publish-Assignment {
    <#
    .SYNOPSIS
    Assigns a built-in or custom policy in Azure.

    .DESCRIPTION
    Assigns a built-in or custom policy in Azure.

    .PARAMETER subscription
    Name of Azure subscription.

    .PARAMETER subscription
    Name of Azure subscription.

    .PARAMETER assignmentName
    Name of policy assignment.

    .PARAMETER policyDisplayName
    The display name of the policy to be assigned.

    .PARAMETER policyParameters
    Hash table of the policy parameters.

    .PARAMETER NonComplianceMessage
    Hash table of non compliance message.

    .EXAMPLE
    $assignmentName = "RestrictResourceGroupLocationPolicyAssignment"
    $subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
    $policyDisplayName = "Allowed locations for resource groups"
    $Locations = Get-AzLocation | where {($_.displayname -like "*europe") -or ($_.displayname -like "uk*")}
    $policyParameters = @{"listOfAllowedLocations"=($Locations.location)}
    $policyParametersString = ($policyParameters['listOfAllowedLocations'] | out-string) -replace "`n","," -replace "`r",""
    $policyParametersString = $policyParametersString.Substring(0,$policyParametersString.Length-1)
    $NonComplianceMessage = @{Message="Resource group location must be in [$policyParametersString]."}

    Publish-Assignment -subscription $subscription `
        -assignmentName $assignmentName `
        -policyDisplayName $policyDisplayName `
        -policyParameters $policyParameters `
        -NonComplianceMessage $NonComplianceMessage

#>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [String]$subscription,
        [Parameter(Mandatory = $true)]
        [String]$assignmentName,
        [Parameter(Mandatory = $false)]
        [boolean]$builtin = $true,
        [Parameter(Mandatory = $true)]
        [String]$policyDisplayName,
        [Parameter(Mandatory = $true)]
        [Hashtable]$policyParameters,
        [Parameter(Mandatory = $true)]
        [Hashtable]$NonComplianceMessage
    )

    Write-Host("Start Publish-Assignment..")

    $subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
    $assignmentScope = "/subscriptions/${subscriptionId}"

    if($builtin)
    {
        write-host "Get built in policy..."
        $Policy = Get-AzPolicyDefinition -BuiltIn | Where-Object {$_.Properties.DisplayName -eq $policyDisplayName}
        write-host "Got built in policy."
    }
    else
    {
        write-host "Get custom policy..."
        $Policy = Get-AzPolicyDefinition -Custom | Where-Object {$_.Properties.DisplayName -eq $policyDisplayName}
        write-host "Got custom policy."
    }

    if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
    {
      write-host "Creating policy assignment $assignmentName as does not exist..."
      New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameterObject $policyParameters -NonComplianceMessage $NonComplianceMessage
      write-host "Created policy assignment $assignmentName."
    }
    else
    {
      write-host "Updating policy assignment $assignmentName as already exists..."
      Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameterObject $policyParameters -NonComplianceMessage $NonComplianceMessage 
      write-host "Updated policy assignment $assignmentName."
    }

    Write-Host("End Publish-Assignment.")
}