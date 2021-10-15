targetScope = 'resourceGroup'

@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff'

@description('Short region name')
param locationshortcode string = 'eun'


//namespace
resource eventHubNamespace 'Microsoft.EventHub/namespaces@2021-01-01-preview' = {
  name: 'schemaregistry-ehns-${locationshortcode}-${namespace}'
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
}
