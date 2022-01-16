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

@description('Short region name')
param locationshortcode string = 'eun'

//storage account
resource datalake 'Microsoft.Storage/storageAccounts@2021-02-01' = {
  name: '${environment}lakesa${locationshortcode}${namespace}'
  location: resourceGroup().location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    isHnsEnabled: true
  }
  tags:  {
    'team' : 'platform'
  }
}

//container
resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2019-06-01' = {
  name: '${datalake.name}/default/lake'
}
