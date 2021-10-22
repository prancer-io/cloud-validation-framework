# Azure ARM Template Unsupported Scenarios

The `prancer-basic` can able to process the Azure ARM templates with it's parameter values. Azure ARM templates provides [`Built-In`](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions) functions to define the attribute values.
The `prancer-basic` currently does not provide supports to process the following `Built-In` functions.

**Array functions**

| Function Name | Reference Link |
|---------------|---------------|
| array | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#array](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#array) |
| contains | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#contains](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#contains) |
| createArray | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#createarray](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#createarray) |
| empty | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#empty](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#empty) |
| first | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#first](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#first) |
| intersection | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#intersection](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#intersection) |
| last | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#last](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#last) |
| length | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#length](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#length) |
| min | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#min](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#min) |
| max | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#max](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#max) |
| range | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#range](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#range) |
| skip | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#skip](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#skip) |
| take | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#take](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#take) |
| union | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#union](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-array#union) |

**Comparison functions**

| Function Name | Reference Link |
|---------------|---------------|
| coalesce | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#coalesce](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#coalesce) |
| less | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#less](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#less) |
| lessOrEquals | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#lessorequals](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#lessorequals) |
| greater | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#greater](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#greater) |
| greaterOrEquals | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#greaterorequals](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-comparison#greaterorequals) |


**Date functions**

| Function Name | Reference Link |
|---------------|---------------|
| dateTimeAdd | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-date#datetimeadd](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-date#datetimeadd) |
| utcNow | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-date#utcnow](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-date#utcnow) |


**Deployment value functions**

| Function Name | Reference Link |
|---------------|---------------|
| deployment | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#deployment](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#deployment) |
| environment | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#environment](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#environment) |
| parameters | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#parameters](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#parameters) |
| variables | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#variables](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#variables) |

**Logical functions**

| Function Name | Reference Link |
|---------------|---------------|
| and | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#and](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#and) |
| bool | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#bool](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#bool) |
| false | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#false](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#false) |
| if | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#if](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#if) |
| not | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#not](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#not) |
| or | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#or](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#or) |
| true | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#true](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-logical#true) |

**Numeric functions**

| Function Name | Reference Link |
|---------------|---------------|
| add | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#add](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#add) |
| copyIndex | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#copyindex](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#copyindex) |
| div | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#div](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#div) |
| float | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#float](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#float) |
| int | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#int](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#int) |
| min | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#min](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#min) |
| max | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#max](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#max) |
| mod | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#mod](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#mod) |
| mul | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#mul](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#mul) |
| sub | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#sub](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-numeric#sub) |

**Object functions**

| Function Name | Reference Link |
|---------------|---------------|
| contains | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#contains](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#contains) |
| createObject | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#createobject](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#createobject) |
| empty | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#empty](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#empty) |
| intersection | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#intersection](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#intersection) |
| json | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#json](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#json) |
| null | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#null](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#null) |
| union | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#union](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-object#union) |


**Resource functions**

| Function Name | Reference Link |
|---------------|---------------|
| extensionResourceId | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#extensionresourceid](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#extensionresourceid) |
| listAccountSas | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#list](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#list) |
| listKeys | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#listkeys](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#listkeys) |
| listSecrets | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#list](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#list) |
| list | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#list](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#list) |
| pickZones | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#pickzones](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#pickzones) |
| deprecated | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#providers](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#providers) |
| reference | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#reference](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#reference) |
| deployments | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#resourcegroup](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#resourcegroup) |
| scope | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#resourceid](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#resourceid) |
| deployments | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#subscription](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#subscription) |
| subscriptionResourceId | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#subscriptionresourceid](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#subscriptionresourceid) |
| tenantResourceId | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#tenantresourceid](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource#tenantresourceid) |


**String functions**

| Function Name | Reference Link |
|---------------|---------------|
| base64 | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#base64](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#base64) |
| base64ToJson | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#base64tojson](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#base64tojson) |
| base64ToString | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#base64tostring](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#base64tostring) |
| concat | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#concat](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#concat) |
| contains | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#contains](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#contains) |
| dataUri | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#datauri](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#datauri) |
| dataUriToString | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#datauritostring](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#datauritostring) |
| empty | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#empty](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#empty) |
| endsWith | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#endswith](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#endswith) |
| first | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#first](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#first) |
| format | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#format](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#format) |
| guid | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#guid](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#guid) |
| indexOf | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#indexof](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#indexof) |
| last | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#last](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#last) |
| lastIndexOf | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#lastindexof](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#lastindexof) |
| length | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#length](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#length) |
| newGuid | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#newguid](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#newguid) |
| padLeft | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#padleft](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#padleft) |
| replace | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#replace](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#replace) |
| skip | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#skip](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#skip) |
| split | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#split](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#split) |
| startsWith | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#startswith](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#startswith) |
| string | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#string](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#string) |
| substring | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#substring](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#substring) |
| take | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#take](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#take) |
| toLower | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#tolower](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#tolower) |
| toUpper | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#toupper](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#toupper) |
| trim | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#trim](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#trim) |
| uniqueString | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uniquestring](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uniquestring) |
| uri | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uri](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uri) |
| uriComponent | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uricomponent](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uricomponent) |
| uriComponentToString | [https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uricomponenttostring](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#uricomponenttostring) |

