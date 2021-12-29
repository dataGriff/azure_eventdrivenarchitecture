targetScope = 'resourceGroup'

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

resource eventHubNamespace 'Microsoft.EventHub/namespaces@2021-01-01-preview' = {
  name: '${environment}-schemaregistry-ehns-${locationshortcode}-${namespace}'
  location: resourceGroup().location
  sku: {
    name: 'Standard'
    tier: 'Standard'
    capacity: 1
  }
  properties: {
    zoneRedundant: true
    isAutoInflateEnabled: true
    kafkaEnabled: true
    maximumThroughputUnits: 20
  }
  tags:  {
    'Team' : 'Platform'
  }
}
