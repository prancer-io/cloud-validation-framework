In an exclusion file, we are defining the test cases that need to be skipped based on resource path, testIDs or both.

There are three types of exclusions supported:

- test exclusion: The exclusionType is set to `test` and field-value is set in `masterTestID`
- resource exclusion: The exclusionType is set to `resource` and the field-value is an array set in `paths`
- single exclusion: The exclusionType is set to `single` and both `masterTestID` and `paths` fields should be present to have combination of these two for exclusion.

``` json
{
  "companyName": "",
  "container": <collection>,
  "fileType": "Exclusion",
  "exclusions": [
    {
      "exclusionType": "resource",
      "paths": [
        "<path of the resource>"
      ]
    },
    {
      "exclusionType": "single",
      "masterTestID": "<TEST_ID>",
      "paths": [
        "<path of the resource>"
      ]
    },
    {
      "exclusionType": "test",
      "masterTestID": "<TEST_ID>"
    }
  ]
}
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| path of the resource | the path of the resource |
| TEST_ID | the masterTestID to be used to exclude |

Here is an example of that:

```json
{
  "companyName": "",
  "container": <collection>,
  "fileType": "Exclusion",
  "exclusions": [
    {
      "exclusionType": "resource",
      "paths": [
        "/test-multi-yaml/multiple-yamls/multiple-helm-response_multiple_yaml_2.yaml"
      ]
    },
    {
      "exclusionType": "single",
      "masterTestID": "TEST_POD_1",
      "paths": [
        "/deployment/deployment-definition.yaml"
      ]
    },
    {
      "exclusionType": "test",
      "masterTestID": "TEST_POD_4"
    }
  ]
}
```
