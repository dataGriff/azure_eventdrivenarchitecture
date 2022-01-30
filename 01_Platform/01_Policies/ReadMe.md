# Setup Policies

In this section we will create [Azure policies](https://docs.microsoft.com/en-us/azure/governance/policy/overview) on our new estate to ensure that team tagging and resource location is in place appropriately from the offset. The team tagging is derived from the fake organisation at [teamconfig](https://github.com/griff182uk/teamconfig) and this team structure has been stored in the [allowedTeams.json](./allowedTeams.json) file for programmatic reference during this section. The team "demo" has been added to this list purely for the quickstart demo purpose as part of this workshop.

If you ever need to quickly cleanup the policies and assignments you have created, please use the script and instructions found [here](./cleanup.ps1).

**You must have all the [pre-requisites](/Prerequisites.md) completed before carrying out the below.**

1. Open up the azure_eventdrivenarchitecture repo in visual studio code.

2. Login to Azure by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
Connect-AzAccount
```

3. Set the azure subscription you are going to be using by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
Set-AzContext -Subscription $subscription
```

4. Assign the built-in policy to ensure only appropriate locations are allowed for resource groups, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$assignmentName = "RestrictResourceGroupLocationPolicyAssignment"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$assignmentScope = "/subscriptions/${subscriptionId}"
$Policy = Get-AzPolicyDefinition -BuiltIn | Where-Object {$_.Properties.DisplayName -eq "Allowed locations for resource groups"}
$Locations = Get-AzLocation | where {($_.displayname -like "*europe") -or ($_.displayname -like "uk*")}
$AllowedLocations = @{"listOfAllowedLocations"=($Locations.location)}
$AllowedLocationsString = ($AllowedLocations['listOfAllowedLocations'] | out-string) -replace "`n","," -replace "`r",""
$AllowedLocationsString = $AllowedLocationsString.Substring(0,$AllowedLocationsString.Length-1)
$NonComplianceMessage = @{Message="Resource group location must be in [$AllowedLocationsString]."}

if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
{
  write-host "Creating policy assignment $assignmentName as does not exist..."
  New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameterObject $AllowedLocations -NonComplianceMessage $NonComplianceMessage
}
else
{
  write-host "Updating policy assignment $assignmentName as already exists..."
  Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameterObject $AllowedLocations -NonComplianceMessage $NonComplianceMessage 
}
```

5. Assign the built-in policy to ensure only appropriate locations are allowed for resources, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$assignmentName = "RestrictResourceLocationPolicyAssignment"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$assignmentScope = "/subscriptions/${subscriptionId}"
$Policy = Get-AzPolicyDefinition -BuiltIn | Where-Object {$_.Properties.DisplayName -eq "Allowed locations"}
$Locations = Get-AzLocation | where {($_.displayname -like "*europe") -or ($_.displayname -like "uk*")}
$AllowedLocations = @{"listOfAllowedLocations"=($Locations.location)}
$AllowedLocationsString = ($AllowedLocations['listOfAllowedLocations'] | out-string) -replace "`n","," -replace "`r",""
$AllowedLocationsString = $AllowedLocationsString.Substring(0,$AllowedLocationsString.Length-1)
$NonComplianceMessage = @{Message="Resource group location must be in [$AllowedLocationsString]."}

if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
{
  write-host "Creating policy assignment $assignmentName as does not exist..."
  New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameterObject $AllowedLocations -NonComplianceMessage $NonComplianceMessage
}
else
{
  write-host "Updating policy assignment $assignmentName as already exists..."
  Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameterObject $AllowedLocations -NonComplianceMessage $NonComplianceMessage 
}
```

6. Assign the built-in policy to ensure that resource groups have to have a team tag, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$assignmentName = "TeamTagRequiredResourceGroupPolicyAssignment"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$assignmentScope = "/subscriptions/${subscriptionId}"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$Policy = Get-AzPolicyDefinition -BuiltIn | Where-Object {$_.Properties.DisplayName -eq "Require a tag on resource groups"}
$tagName = "team"
$teamTag = @{"tagName"=$tagName}
$NonComplianceMessage = @{Message="Resource group must have a team tag."}

if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
{
  write-host "Creating policy assignment $assignmentName as does not exist..."
  New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameterObject $teamTag -NonComplianceMessage $NonComplianceMessage
}
else
{
  write-host "Updating policy assignment $assignmentName as already exists..."
  Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameterObject $teamTag -NonComplianceMessage $NonComplianceMessage
}
```

7. Assign the built-in policy to ensure that resources have to have a team tag, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$assignmentName = "TeamTagRequiredResourcePolicyAssignment"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$assignmentScope = "/subscriptions/${subscriptionId}"
$Policy = Get-AzPolicyDefinition -BuiltIn | Where-Object {$_.Properties.DisplayName -eq "Require a tag on resources"}
$tagName = "team"
$teamTag = @{"tagName"=$tagName}
$NonComplianceMessage = @{Message="Resources must have a team tag."}

if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
{
  write-host "Creating policy assignment $assignmentName as does not exist..."
  New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameterObject $teamTag -NonComplianceMessage $NonComplianceMessage
}
else
{
  write-host "Updating policy assignment $assignmentName as already exists..."
  Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameterObject $teamTag -NonComplianceMessage $NonComplianceMessage 
}
```

8. Create a custom policy to ensure that resource group team tag values are from an appropriate list, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$location = [System.Environment]::GetEnvironmentVariable("AZURE_REGION")
New-AzSubscriptionDeployment `
  -Name eventPolicyResourceGroup `
  -Location $location  `
  -TemplateFile 01_Platform\01_Policies\bicep\policyTagValueResourceGroups.bicep
```

9. Assign the custom policy to ensure that resource groups have a valid team tag value, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$assignmentName = "TeamTagValueDenyResourceGroupPolicyAssignment"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$assignmentScope = "/subscriptions/${subscriptionId}"
$Policy = Get-AzPolicyDefinition -Custom | Where-Object {$_.Properties.DisplayName -eq "Deny deployment of resource group if tag values are not in given list"}
$teamValues = (Get-Content 01_Platform\01_Policies\AllowedTeams.json | ConvertFrom-Json).tagValues.value
$teamValues = $teamValues  -replace " ",","
$NonComplianceMessage = @{Message="Resources group must have a team tag value in $teamValues."}

if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
{
  write-host "Creating policy assignment $assignmentName as does not exist..."
  New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameter 01_Platform\01_Policies\AllowedTeams.json -NonComplianceMessage $NonComplianceMessage
}
else
{
  write-host "Updating policy assignment $assignmentName as already exists..."
  Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameter 01_Platform\01_Policies\AllowedTeams.json -NonComplianceMessage $NonComplianceMessage 
}
```

10. Create a custom policy to ensure that resources team tag values are from an appropriate list, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$location = [System.Environment]::GetEnvironmentVariable("AZURE_REGION")
New-AzSubscriptionDeployment `
  -Name eventPolicyResourceGroup `
  -Location $location  `
  -TemplateFile 01_Platform\01_Policies\bicep\policyTagValueResources.bicep
```

11. Assign the custom policy to ensure that resource groups have a valid team tag value, by highlighting the code below, press F1 and select or type **Powershell: Run Selection**.

```ps1
$assignmentName = "TeamTagValueDenyResourcePolicyAssignment"
$subscription = [System.Environment]::GetEnvironmentVariable("AZURE_SUBSCRIPTION") 
$subscriptionId = (Get-AzSubscription -SubscriptionName $subscription).id
$assignmentScope = "/subscriptions/${subscriptionId}"
$Policy = Get-AzPolicyDefinition -Custom | Where-Object {$_.Properties.DisplayName -eq "Deny deployment of resource if tag values are not in given list"}
$teamValues = (Get-Content 01_Platform\01_Policies\AllowedTeams.json | ConvertFrom-Json).tagValues.value
$teamValues = $teamValues  -replace " ",","
$NonComplianceMessage = @{Message="Resources must have a team tag value in $teamValues."}

if (-Not (Get-AzPolicyAssignment -Name $assignmentName -ErrorAction SilentlyContinue))
{
  write-host "Creating policy assignment $assignmentName as does not exist..."
  New-AzPolicyAssignment -Name $assignmentName -PolicyDefinition $Policy -Scope $assignmentScope -PolicyParameter 01_Platform\01_Policies\AllowedTeams.json -NonComplianceMessage $NonComplianceMessage
}
else
{
  write-host "Updating policy assignment $assignmentName as already exists..."
  Set-AzPolicyAssignment -Name $assignmentName -Scope $assignmentScope -PolicyParameter 01_Platform\01_Policies\AllowedTeams.json -NonComplianceMessage $NonComplianceMessage 
}
```
