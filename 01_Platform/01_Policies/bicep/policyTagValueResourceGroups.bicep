targetScope = 'subscription'

var policyName = 'deny-resource-group-tag-and-values'
var policyDisplayName = 'Deny deployment of resource group if tag values are not in given list'
var policyDescription = 'Deny deployment of resource group if tag values are not in given list'

resource policy 'Microsoft.Authorization/policyDefinitions@2020-09-01' = {
  name: policyName
  properties: {
    displayName: policyDisplayName
    description: policyDescription
    policyType: 'Custom'
    mode: 'Indexed'
    metadata: {
      category: 'Tags'
    }

    parameters: {
      tagName: {
        type: 'String'
        metadata: {
          displayName: 'Tag name'
          description: 'A tag to audit'
        }
      }
      tagValues: {
        type: 'Array'
        metadata: {
          displayName: 'Tag Values'
          description: 'A list of allowed tag values' // Use backslash as an escape character for single quotation marks
        }
      }
    }
    policyRule: {
      if:{
      allOf: [
          {
            field: 'type'
            equals:'Microsoft.Resources/subscriptions/resourceGroups'
          }
          {
            field: '[concat(\'tags[\', parameters(\'tagName\'), \']\')]' // No need to use an additional forward square bracket in the expressions as in ARM templates
            notIn: '[parameters(\'tagValues\')]'
          }
        ]
      }
      then: {
        effect: 'Deny'
      }
    }
  }
}
