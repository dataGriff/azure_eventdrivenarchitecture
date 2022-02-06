targetScope = 'subscription'

@description('Environment for your resources')
@allowed([
  'dv'
  'qa'
  'lv'
])
param environment string = 'dv'

@description('Region for your resources')
param location string = 'northeurope'

resource resourceGroup1 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-broker-rg'
  location: location
  tags:  {
    'team' : 'platform'
  }
}

resource resourceGroup2 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-schemaregistry-rg'
  location: location
  tags:  {
    'team' : 'platform'
  }
}

resource resourceGroup3 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-lake-rg'
  location: location
  tags:  {
    'team' : 'platform'
  }
}

resource resourceGroup4 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-databricks-rg'
  location: location
  tags:  {
    'team' : 'platform'
  }
}

resource resourceGroup5 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-sql-rg'
  location: location
  tags:  {
    'team' : 'platform'
  }
}

resource resourceGroup6 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-account-rg'
  location: location
  tags:  {
    'team' : 'customer'
  }
}

resource resourceGroup7 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-contact-rg'
  location: location
  tags:  {
    'team' : 'customer'
  }
}

resource resourceGroup8 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-product-rg'
  location: location
  tags:  {
    'team' : 'product'
  }
}

resource resourceGroup9 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-leads-rg'
  location: location
  tags:  {
    'team' : 'conversions'
  }
}

resource resourceGroup10 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-salesfiles-rg'
  location: location
  tags:  {
    'team' : 'conversions'
  }
}

resource resourceGroup11 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${environment}-events-sales-rg'
  location: location
  tags:  {
    'team' : 'conversions'
  }
}








