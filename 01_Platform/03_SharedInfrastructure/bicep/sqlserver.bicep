//Taken From:
//https://www.keepsecure.ca/blog/a-first-look-at-bicep/

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

@description('SQL Admin Password')
param sqlAdministratorLoginPassword string

@description('Client IP Address')
param clientIpAddress string

var sqlServerName = '${environment}-events-sql-${locationshortcode}-${namespace}'
var minTlsVersion = '1.2' // Should always be latest supported TLS version
var sqlAdministratorLogin = 'admin-${sqlServerName}' // Using AAD auth, so create random user

resource sqlServer 'Microsoft.Sql/servers@2019-06-01-preview' = {
  name: sqlServerName
  location: location
  properties: {
    administratorLogin: sqlAdministratorLogin
    administratorLoginPassword: sqlAdministratorLoginPassword
    version: '12.0'
    minimalTlsVersion: minTlsVersion
  }
  tags:  {
    'team' : 'platform'
  }
}

resource fwRule 'Microsoft.Sql/servers/firewallRules@2015-05-01-preview' = {
    name: '${sqlServer.name}/clientAllow'
    properties: {
        startIpAddress: clientIpAddress
        endIpAddress: clientIpAddress
    }
}
