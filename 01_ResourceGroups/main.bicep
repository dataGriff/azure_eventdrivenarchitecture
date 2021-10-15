targetScope = 'subscription'

param location string = 'northeurope'

resource resourceGroup1 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-leads-rg'
  location: location
}

resource resourceGroup2 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-salesfiles-rg'
  location: location
}

resource resourceGroup3 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-sales-rg'
  location: location
}

resource resourceGroup4 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-customer-rg'
  location: location
}

resource resourceGroup5 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-broker-rg'
  location: location
}

resource resourceGroup6 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-schemaregistry-rg'
  location: location
}

resource resourceGroup7 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-lake-rg'
  location: location
}

resource resourceGroup8 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: 'events-databricks-rg'
  location: location
}






