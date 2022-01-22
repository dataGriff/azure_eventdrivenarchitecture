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

@description('Event name for hub and container')
param eventhubname string

@description('Name of the consumer of the event')
param consumer string

@description('Name of the team consuming the event')
param teamname string

var ehnamespace = '${environment}-events001-ehns-${locationshortcode}-${namespace}'


resource symbolicname 'Microsoft.EventHub/namespaces/eventhubs/consumergroups@2021-06-01-preview' = {
  name: '${ehnamespace}/${eventhubname}/${consumer}'
  properties: {
    userMetadata: 'team : ${teamname}'
  }
}
