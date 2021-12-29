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

@description('This will be the event hub name and for the corresponding container. This is usually the aggregate that events are being recorded against.')
param eventhubname string

@description('Duration immutability lasts for in days')
param immutabilitydays int = 7

@description('Event hub capture period in seconds')
param eventhubcaptureseconds int = 300

@description('Event hub capture maximum in bytes')
param eventhubcapturebytes int = 300000000

@description('Event hub partitions')
param eventhubpartitions int = 4

@description('Event hub retention in days')
param eventhubretentiondays int = 7

var storageaccount = '${environment}events001sa${locationshortcode}${namespace}'
var ehnamespace = '${environment}-events001-ehns-${locationshortcode}-${namespace}'

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2019-06-01' = {
  name: '${storageaccount}/default/${eventhubname}'
}

resource immutable 'Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies@2019-04-01' = {
  name: '${storageaccount}/default/${eventhubname}/default'
  properties: {
    immutabilityPeriodSinceCreationInDays: immutabilitydays
  }
  dependsOn: [
    container
    eventhub
    send
    listen
  ]
}

//Event Hub with Capture
resource eventhub 'Microsoft.EventHub/namespaces/eventhubs@2021-06-01-preview' = {
  name: '${ehnamespace}/${eventhubname}'
  properties: {
    captureDescription: {
      destination: {
        name: 'EventHubArchive.AzureBlockBlob'
        properties: {
          archiveNameFormat: '{EventHub}/{Year}/{Month}/{Day}/{Hour}/{EventHub}_{Year}_{Month}_{Day}_{Hour}_{Minute}_{Second}_{PartitionId}_{Namespace}'
          blobContainer: eventhubname
          storageAccountResourceId: '/subscriptions/${subscription().subscriptionId}/resourceGroups/${resourceGroup().name}/providers/Microsoft.Storage/storageAccounts/${storageaccount}'
        }
      }
      enabled: true
      encoding: 'Avro'
      intervalInSeconds: eventhubcaptureseconds
      sizeLimitInBytes: eventhubcapturebytes
      skipEmptyArchives: true
    }
    messageRetentionInDays: eventhubretentiondays
    partitionCount: eventhubpartitions
  }
  dependsOn: [
    container
  ]
}

resource send 'Microsoft.EventHub/namespaces/eventhubs/authorizationRules@2021-01-01-preview' = {
  parent: eventhub
  name: 'send'
  properties: {
    rights: [
      'Send'
    ]
  }
}

resource listen 'Microsoft.EventHub/namespaces/eventhubs/authorizationRules@2021-01-01-preview' = {
  parent: eventhub
  name: 'listen'
  properties: {
    rights: [
      'Listen'
    ]
  }
}
