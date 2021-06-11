# Run Prancer CLI

Here are the examples of run crawler and compliance in different ways.

- Clone this repository, [https://github.com/prancer-io/prancer-hello-world](https://github.com/prancer-io/prancer-hello-world)
- Check the `config.ini file`, here you can see the value of `containerFolder` in `TESTS` section is `./validation/`.
It means all the testcases are stored inside the `validation` directory.

1) Run Crawler Only

```
prancer scenario-arm-pass --crawler --db=NONE
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection which contains master snapsshot and mastertest files. |
| --crawler | Specifies that you want to run crawler only on given collection. |
| --db=None | It defines that the prancer have to find the collection of mastersnapshot and mastertest from local filesystem. |

- On completion of crawler it generates the snapshot file inside the collection with name `<mastersnapshot_name>_gen.json`.

2) Run Compliance Only

```
prancer scenario-arm-pass --compliance --db=NONE
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection on which you want to run the compliance. |
| --compliance | Specifies that you want to run compliance only on given collection. |
| --db=None | It defines that the prancer have to find the collection of snapshot and mastertest files from local filesystem. |

- On completion of compliance, it generates the `snapshots` folder inside the collection which contains the actual snapshot files of your cloud resources or templates files for IaC. It also creates the outputs file named `output-<mastertest_name>.json` which contains the `passed` and `failed` results of compliance.

3) Run both crawler and compliance.

```
prancer scenario-arm-pass --db=NONE
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection on which you want to run the compliance. |
| --db=None | It defines that the prancer have to find the collection of snapshot and mastertest files from local filesystem. |

- If you doesn't defines the `--crawler` or `--compliance` then it runs both proceesses. First it crawls the collection and generates the snapshot file.After it runs the compliance on it and generates the output file.