targetScope = 'resourceGroup'

@description('Environment for your resources')
@allowed([
  'dv'
  'qa'
  'lv'
])
param environment string = 'dv'

@description('Unique postfix for your resources to ensure globally unique')
param namespace string

@description('Location of the resources')
param location string = resourceGroup().location

@description('Short region name')
param locationshortcode string = 'eun'

@description('Short region name')
param daysToDeleteData int = 7

@description('Short region name')
param daysToArchiveData int = 5

@description('Short region name')
param daysToCoolData int = 3

var daysToRestoreFiles = daysToCoolData - 1
var daysToRestoreContainer = daysToCoolData

resource eventHubNamespace 'Microsoft.EventHub/namespaces@2021-01-01-preview' = {
  name: '${environment}-events001-ehns-${locationshortcode}-${namespace}'
  location: location
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
    'team' : 'platform'
  }
}

resource send 'Microsoft.EventHub/namespaces/authorizationRules@2021-06-01-preview' = {
  parent: eventHubNamespace
  name: 'send'
  properties: {
    rights: [
      'Send'
    ]
  }
}

resource listen 'Microsoft.EventHub/namespaces/authorizationRules@2021-06-01-preview' = {
  parent: eventHubNamespace
  name: 'listen'
  properties: {
    rights: [
      'Listen'
    ]
  }
}

resource eventstorage 'Microsoft.Storage/storageAccounts@2021-02-01' = {
  name: '${environment}events001sa${locationshortcode}${namespace}'
  location: location
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
    'team' : 'platform'
  }
}

resource lifecycle 'Microsoft.Storage/storageAccounts/managementPolicies@2019-04-01' = {
  name: 'default'
  parent: eventstorage
  properties: {
    policy: {
      rules: [
        {
          definition: {
            actions: {
              baseBlob: {
                delete: {
                  daysAfterModificationGreaterThan: daysToDeleteData
                }
                tierToArchive: {
                  daysAfterModificationGreaterThan: daysToArchiveData
                }
                tierToCool: {
                  daysAfterModificationGreaterThan: daysToCoolData
                }
              }
            }
            filters: {
              blobTypes: [
                'blockBlob'
              ]
            }
          }
          enabled: true
          name: 'eventsLifecycle'
          type: 'Lifecycle'
        }
      ]
    }
  }
}

resource blobservice 'Microsoft.Storage/storageAccounts/blobServices@2021-06-01' = {
  name: 'default'
  parent: eventstorage
  properties: {
    automaticSnapshotPolicyEnabled: true
    changeFeed: {
      enabled: true
      retentionInDays: daysToRestoreContainer
    }
    containerDeleteRetentionPolicy: {
      days: daysToDeleteData
      enabled: true
    }
    deleteRetentionPolicy: {
      days: daysToDeleteData
      enabled: true
    }
    isVersioningEnabled: true
    restorePolicy: {
      days: daysToRestoreFiles
      enabled: true
    }
  }
}
