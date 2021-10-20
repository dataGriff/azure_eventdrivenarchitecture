targetScope = 'resourceGroup'

@description('Unique postfix for your resources to ensure globally unique')
param namespace string = 'griff2'

@description('Short region name')
param locationshortcode string = 'eun'

@description('Event name for hub and container')
param event string

@description('Name of the consumer of the event')
param consumer string

@description('Name of the team cosuming the event')
param teamname string = 'Fake Team'

var ehnamespace = 'events001-ehns-${locationshortcode}-${namespace}' 


resource symbolicname 'Microsoft.EventHub/namespaces/eventhubs/consumergroups@2021-06-01-preview' = {
  name: '${ehnamespace}/${event}/${consumer}'
  properties: {
    userMetadata: 'Team Name : ${teamname}'
  }
}
