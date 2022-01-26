**How to use Prancer Enterprise APIs**
===

Here is the steps about how to generate access token and access prancer enterprise apis.

## 1) Generate API Token:

API tokens are being used to connect to the Prancer tenant programmatically. You can generate multiple tokens for different purposes.
the following use cases can be covered by generating tokens:

 - connecting to Prancer API
 - running VSCode extension
 - connecting from CI tools

### How to generate tokens
Login to the Prancer Portal, On the user menu (top right), select the drop-down menu and select `User Access Token`.

![../images/token/token1.png](../images/token/token1.png)

Click on `New Token` to generate a new token. Make sure you keep the token somewhere safe, you cannot retrieve it when you close the page.

![../images/token/token2.png](../images/token/token2.png)

## 2) Call the authntication API

Call [Validate Access Token](authentication.md#validate-access-token) API to validate your token and get the authenticated JWT Bearer token to access APIs.

![../images/token/validate_access_token.png](../images/token/validate_access_token.png)

## 3) Access the Prancer Enterprise API

You got the authenticated `JWT Bearer token` by calling Validate Access Token API. Now you can use it to call APIs of Prancer Enterprise. For example,

- Call the [Get Collection List](collection.md#collection-get) API for get all collections list.

![../images/api/collection_list.png](../images/api/collection_list.png)

- Call the [Run compliance](compliance.md#compliance-run-compliance) API to run compliance on a collection.

![../images/api/run_compliance.png](../images/api/run_compliance.png)