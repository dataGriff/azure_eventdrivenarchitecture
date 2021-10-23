@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff'

@description('Short region name')
param locationshortcode string = 'eun'

//storage account
resource storage 'Microsoft.Storage/storageAccounts@2021-02-01' = {
  name: 'salessa${locationshortcode}${namespace}'
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
}

//Storage Account Container
resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2019-06-01' = {
  name: '${storage.name}/default/sales'
}

