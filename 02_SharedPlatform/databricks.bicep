@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff'

@description('Full region name')
param location string = 'northeurope'

@description('Short region name')
param locationshortcode string = 'eun'

@description('Databricks SKU')
param sku string = 'premium'

var databricksWorkspaceName = 'events-dbw-${locationshortcode}-${namespace}'
var managedResourceGroupName = 'databricks-rg-${databricksWorkspaceName}-${uniqueString(databricksWorkspaceName, resourceGroup().id)}'

resource databricks 'Microsoft.Databricks/workspaces@2018-04-01' = {
  name: databricksWorkspaceName
  location: location
  sku: {
    name: sku
  }
  properties: {
    managedResourceGroupId: subscriptionResourceId('Microsoft.Resources/resourceGroups', managedResourceGroupName)
    authorizations: []
  }
}

output databricksWorkspaceName string = databricksWorkspaceName
output workspaceUrl string = databricks.properties.workspaceUrl
