targetScope = 'resourceGroup'

@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff2'

@description('Short region name')
param locationshortcode string = 'eun'

@description('Event name for hub and container')
param event string

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

var storageaccount = 'events001sa${locationshortcode}${namespace}'
var ehnamespace = 'events001-ehns-${locationshortcode}-${namespace}' 

//Storage Account Container
resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2019-06-01' = {
  name: '${storageaccount}/default/${event}'
}

resource immutable 'Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies@2019-04-01' = {
  name: '${storageaccount}/default/${event}/default'
  properties: {
    immutabilityPeriodSinceCreationInDays: immutabilitydays
  }
}

//Event Hub with Capture
resource symbolicname 'Microsoft.EventHub/namespaces/eventhubs@2021-06-01-preview' = {
  name: '${ehnamespace}/${event}'
  properties: {
    captureDescription: {
      destination: {
        name: 'EventHubArchive.AzureBlockBlob'
        properties: {
          archiveNameFormat: '{EventHub}/{Year}/{Month}/{Day}/{EventHub}_{Year}_{Month}_{Day}_{Hour}_{Minute}_{Second}_{PartitionId}_{Namespace}'
          blobContainer: event
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
}
