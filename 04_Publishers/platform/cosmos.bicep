@description('Cosmos DB account name, max length 44 characters, lowercase')
param accountName string = 'customer-cosdb-eun-griff2'

@description('Location for the Cosmos DB account.')
param location string = resourceGroup().location

@description('Name of team that owns cosmos db account.')
param teamName string

@description('The default consistency level of the Cosmos DB account.')
@allowed([
  'Eventual'
  'ConsistentPrefix'
  'Session'
  'BoundedStaleness'
  'Strong'
])
param defaultConsistencyLevel string = 'Session'

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2021-04-15' = {
  name: accountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: defaultConsistencyLevel
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    databaseAccountOfferType: 'Standard'
  }
  tags:  {
    'Team' : teamName
  }
}

