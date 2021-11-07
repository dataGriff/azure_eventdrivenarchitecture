targetScope = 'resourceGroup'

@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff'

@description('Short region name')
param locationshortcode string = 'eun'


//namespace
resource eventHubNamespace 'Microsoft.EventHub/namespaces@2021-01-01-preview' = {
  name: 'events001-ehns-${locationshortcode}-${namespace}'
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

//auth rule send
resource send 'Microsoft.EventHub/namespaces/authorizationRules@2021-06-01-preview' = {
  parent: eventHubNamespace
  name: 'send'
  properties: {
    rights: [
      'Send'
    ]
  }
  dependsOn: [
    eventHubNamespace
  ]
}

//auth rule send
resource listen 'Microsoft.EventHub/namespaces/authorizationRules@2021-06-01-preview' = {
  parent: eventHubNamespace
  name: 'listen'
  properties: {
    rights: [
      'Listen'
    ]
  }
  dependsOn: [
    eventHubNamespace
  ]
}

//storage account
resource eventstorage 'Microsoft.Storage/storageAccounts@2021-02-01' = {
  name: 'events001sa${locationshortcode}${namespace}'
  location: resourceGroup().location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
  tags:  {
    'Team' : 'Platform'
  }
}
