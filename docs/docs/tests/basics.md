A test file is the final element you need to configure to get **Prancer** going. A test file defines multiple items that we'll discover below.

# Basic structure

To configure a test, create a file named `test.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `test.json`

The basic structure of a test file starts out with meta information like so:

```json
    {
        "contentVersion": "1.0.0.0",
        "fileType": "test",
        "notification": [],
        "snapshot": "<snapshot-to-use>",
        "tests": []
    }
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| snapshot-to-use | Name of the snapshot to use, it can be a full filename with extension in the current directory of the test file or be stored in the **MongoDB** database under a name similar to the filename but without extension. |
| notification | Notification only works in Enterprise Version |

# Tests

The `tests` collection of the `root` element contains all of the tests to run against the selected snapshot. You can consider each test in this collection as a unit test or integration test of some sorts. Each test in the collection is defined using the following structure:

```json
    {
        "testName": "<name-of-test>",
        "version": "0.1",
        "cases": []
    }
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| name-of-test | Put a readable name in there for future reference |

You should create as many tests as you need. Each test should properly declare what you are trying to achieve such as:

- Ensure my network uses a CIDR block of `172.10.0.0/16`
- Ensure my security group opens port `22` only to office users
- Ensure my virtual machine is configured to terminate on stop
- etc

# Test case

The `cases` collection of each `test` contains the final element that will be doing all of the work(i.e. Rules).

A test case is just a container for a rule and a test id but may contain more information later on, this is why we didn't create just a collection of rules instead.

To define a `case`, use the following structure:

```json
    {
        "testId": "<test-case-name>",
        "rule": "<rule>"
    }
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| test-case-name | A unique identifier for this test-case |
| rule | The rule to execute, see below for more information |

# Rules

A rule is an expression that we parse using very standard programing syntax(Javascript style with single equals for comparison).

Rules usually refer to a snapshot that you made earlier in the process. To refer to a snapshot, you must use the curly braces with the name of the snapshot between them like so:
`{securityGroup4Snapshot}.property1.property2.propertyN`

You can specify any chain of properties in there. Later in the process, you will see how you can inspect the **MongoDB** database to see the data that gets collected and how you can build your rules.

A rule must yield a `Boolean` value, either from a single operand function or through the use of a complex multi-operand/operator form.</br>
For example:

    exists({securityGroup4Snapshot}.property1)
    {securityGroup4Snapshot}.property1 = 'foo'
    1 = 0

Here are all of the points your rule should follow:

1. Rules should refer to a snapshot
2. Rules are assumed to contain a **left hand side** operand, an **operator** and a **right hand side** operand
3. Rules should contain an **operator**, if the **operator** is missing, it is assumed to be the **equality** `=` operator 
4. Rules without a **right hand side** operand are assumed to be a `True` value

# Data types

**Prancer** uses only a basic set of data types that matches [Python's basic data types](https://docs.python.org/3/library/stdtypes.html):

1. `Integer` or `Float` for all types of numbers
2. `String` using the single quote delimiter only
3. `List` (Other programming languages may call this an `Array` or a `Collection`)
4. `Dictionary` (Other programming languages may call this `HashMap`, `Object` or even an `Array`)

You can compare any two similar types together easily by using the **equality** `=` operator. When comparing different types, a type casting will be attempted. All type casting follows the **Python** rules:

* `Integer` are casted to `Float` when compared to a `Float`
* `Integer` or `Float` are transformed to a `String` when compared to a `String`
* `List` and `Dictionary` are stringified when compared to a `String`
* etc

Refer to the official [Python Built-in types](https://docs.python.org/3/library/stdtypes.html) documentation page to know more.

# Full example

Here is a full example of what a test file could look like:

```json
    {
        "contentVersion": "1.0.0.0",
        "fileType": "test",
        "notification": [
            {
                "type": "slack",
                "address": "group-name"
            },
            {
                "type": "email",
                "address": "name@domain.com"
            }
        ],
        "snapshot": "snapshot1",
        "testSet": [
            {
                "testName": "test1",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "exists({11}.location)"
                    },
                    {
                        "testId": "2",
                        "rule": "{11}.location='eastus2'"
                    },
                    {
                        "testId": "3",
                        "rule": "exists({12}.properties.addressSpace.addressPrefixes[])"
                    }
                ]
            }
        ]
    }
```

> **Note**: Remember that everything inside `{}` must be exactly the same as the snapshotId which defined earlier.
