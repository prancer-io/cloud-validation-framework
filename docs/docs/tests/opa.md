# Open Policy Agent (OPA) Integration

**Prancer** Cloud Validation framework has built-in simple and robust classic rule engine to write test rules to validate the cloud resources. However, with the industry adopting a standard method of writing policy rules and their evaluation, **Prancer** has integrated **OPA** (Open Policy Agent) and its rule language (**REGO**) support to write and evaluate policy rules. By leveraging **OPA** in **Prancer framework**, it gives us the capability to write complex rules to evaluate cloud resources.

## Requirements for OPA

- **OPA** has been integrated as a binary executable. This executable has to be downloaded and installed with an execute permission.
- Update **Prancer** config.ini with a separate section as:

```ini
  [OPA]
  opa=true
  opaexe=<Path to the OPA binary>
```

- **OPA** rules can be written embedded in a test case or as a separate rego file. The examples of a classic rule and rego embedded rule in the framework are as:

```json
{ 
    "testId": "2",
    "rule":"{TEST_RESOURCE_JSON_ID}.SecurityGroups[0].GroupName='launch-wizard-1'"
},
{
    "testId": "3",
    "type": "rego",
    "rule": "input.SecurityGroups[0].GroupName=\"launch-wizard-1\"",
    "snapshotId": ["TEST_RESOURCE_JSON_ID"],
    "eval": "data.rule.rulepass"
}
```

- If you have a master test file, you should use "masterSnapshotId" instead of "snapshotId"

   The classic rule has an expression with a Left Hand Side(LHS) and Right Hand Side(RHS) with a comparator operator. The classic rule engine evaluates LHS and RHS, uses the comparator to evaluate the rule.

   The Rego rule has an evaluation for a policy and the default has been set to "data.rule.rulepass" and this is evaluated for true value for a test to pass. The rule type has to be specified as "rego" for backward compatibility of the framework.

- *OPA* rules can also be written in a separate rego file. The examples of a classic rule and rego rule written in a separate file in the framework are as:

```json
{
    "testId": "1",
    "rule":"exist({TEST_RESOURCE_JSON_ID}.SecurityGroups)"
},
{
    "testId": "4",
    "type": "rego",
    "rule": "file(ruleexists.rego)",
    "snapshotId": ["TEST_RESOURCE_JSON_ID"],
    "eval": "data.rule.rulepass"
}
```

And here is the `ruleexists.rego`:

```txt
package rule
default rulepass = true
rulepass = false{
    is_null(input.SecurityGroups)
}
```

The file ruleexists.rego should exist in the same directory (container) as the test files.

### References

- OPA documentation - [https://www.openpolicyagent.org/docs/latest/](https://www.openpolicyagent.org/docs/latest/).
- **Prancer** command line toolset with OPA - [https://github.com/prancer-io/cloud-validation-framework](https://github.com/prancer-io/cloud-validation-framework)
