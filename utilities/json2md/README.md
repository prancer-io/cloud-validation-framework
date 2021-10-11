# JSON to Markdown

## 1. Install required packages

- This tool requires python3, please download and install it in your machine

- Run following command in your bash shell

```bash
cd json2md

make install
```

## 2. How to run the tool?

source json2md_venv/bin/activate


export PATH_PREFIX=https://github.com/Azure/azure-quickstart-templates/tree/master
export REGO_PREFIX=https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/

python json2md.py --template templateAzureQuickstart.md --input output-master-test.json

```
usage: json2md.py [-h] [--template TEMPLATE] --input INPUT [--output OUTPUT]

optional arguments:
  -h, --help           show this help message and exit
  --template TEMPLATE  Template file
  --input INPUT        Path to json data
  --output OUTPUT      Write to markdown file

```

- Example:
```bash
./json2md.py --input sample/output-master-test.json --template template.md --output output-master-test.md
```