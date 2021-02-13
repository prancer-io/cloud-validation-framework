Once you run a test, it will generate an output file in the container's directory. This file is always called `output-xyz.json` where the `xyz.json` is the original test file name.

# Structure of output files

The structure of an output test file always looks like this:

    {
        "contentVersion": "1.0.0.0",
        "fileType": "output",
        "timestamp": 1555342894792,
        "snapshot": "snapshot",
        "container": "container1",
        "test": "test",
        "results": []
    }

Here is a description of the different items you will find in this file:

| Field | Description |
|-----|-------------------|
| contentVersion | The version of the rule engine used to parse the rule |
| timestamp | Epoch timestamp when this file was generated |
| snapshot | Name of the snapshot that was used |
| container | Name of the container used in this test |
| test | Name of the test that was used |
| results | The results of all tests ran, see below for more information |

# Results

The results section contains all the result of each test case that was run in one big list. Each result contains information regarding the testcase so you can see what was the result and what information it used to run the test. Here is an example with field by field explanations:

    {
        "result": "failed",
        "snapshots": [],
        "testId": "1",
        "rule": "{1}.Vpcs[0].CidrBlock='172.31.0.0/16'"
    }

| Field | Description |
|-----|-------------------|
| result | Reports if the test case was a `passed` or a `failed` (failure) |
| snapshots | An array of all snapshots that were used in rule. See below for more information. |
| testId | The name of the test case that generated this result |
| rule | The rule that was used to run this test |

# Snapshots

The `snapshots` section of a test result contains all the information you would need to debug a failed test. Here is an example with an explanation of the fields:

    {
        "id": "1",
        "path": "",
        "structure": "aws",
        "reference": "",
        "source": "awsStructure"
    }

| Field | Description |
|-----|-------------------|
| id | Name of the snapshot that was used as part of the rule |
| path | The path that this snapshot refers to (`Azure` and `Git` only) |
| structure | The type of snapshot |
| reference | **TBD** |
| source | The connector name that was used to retrieve the data |