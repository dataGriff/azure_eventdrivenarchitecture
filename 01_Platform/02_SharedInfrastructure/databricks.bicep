@description('Environment for your resources')
@allowed([
  'dv'
  'qa'
  'lv'
])
param environment string = 'dv'

@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff'

@description('Short region name')
param locationshortcode string = 'eun'

@description('Databricks SKU')
param sku string = 'premium'

var databricksWorkspaceName = '${environment}-events-dbw-${locationshortcode}-${namespace}'
var managedResourceGroupName = '${databricksWorkspaceName}-rg-${uniqueString(databricksWorkspaceName, resourceGroup().id)}'

resource databricks 'Microsoft.Databricks/workspaces@2018-04-01' = {
  name: databricksWorkspaceName
  location: resourceGroup().location
  sku: {
    name: sku
  }
  properties: {
    managedResourceGroupId: subscriptionResourceId('Microsoft.Resources/resourceGroups', managedResourceGroupName)
    authorizations: []
  }
  tags:  {
    'Team' : 'Platform'
  }
}

output databricksWorkspaceName string = databricksWorkspaceName
output workspaceUrl string = databricks.properties.workspaceUrl
