#! json2md_venv/bin/python3

import argparse
import json
import os
import re

import pandas as pd
from urllib.parse import urljoin
from jinja2 import Environment, FileSystemLoader

meta_key = 'meta'
result_key = 'results'
meta_keys = ['timestamp', 'snapshot', 'container', 'test']
table_keys = ['snapshots', 'tags']

path_prefix=os.environ.get('PATH_PREFIX')
rego_prefix=os.environ.get('REGO_PREFIX')


def valid_path(s):
    if not os.path.isfile(s):
        raise argparse.ArgumentTypeError("Not exist path: {0}.".format(s))
    return s


def list_to_table(list_value):
    tb = pd.json_normalize(list_value)
    if path_prefix is not None and 'paths' in tb.columns:
        tb['paths'] = tb['paths'].apply(lambda x: [f'{path_prefix}{i}' for i in x])

    tb = tb.T.reset_index()
    tb.columns = ['Title', 'Description']
    return tb.to_markdown(index=False)


def prepare_data(data):

    # form metadata
    meta_data = list_to_table({key: data.get(key) for key in meta_keys})

    # form the message result
    if result_key not in data:
        raise ValueError(f"[ERROR] JSON data doesn't has key: {result_key}. Check your json file or update the result_key in script")
        # sys.exit(1)

    results = data[result_key]
    for i in range(len(results)):
        if rego_prefix is not None and 'rule' in results[i]:
            file_name = re.search(r"file\((.*)\)", results[i]['rule']).group(1)
            results[i]['rule'] = f"file({urljoin(rego_prefix, file_name)})"

        for key in table_keys:
            try:
                results[i][key] = list_to_table(results[i][key])
            except KeyError:
                print(f"[WARNING] JSON data doesn't has key: {key}. Your output might not completed as expectation")

    # update data
    data[meta_key] = meta_data

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', help="Template file", type=str, default="template.md")
    parser.add_argument('--input', help="Path to json data", type=valid_path, required=True)
    parser.add_argument('--output', help="Write to markdown file", type=str, default="output.md")

    args, _ = parser.parse_known_args()
    # print(args)

    env = Environment(loader=FileSystemLoader('.'))
    rtemplate = env.get_template(args.template)

    with open(args.input) as f:
        data = json.load(f)

    rtemplate.stream(data=prepare_data(data)).dump(args.output)
    print(f"Completed! Your MD file at: {args.output}")


if __name__ == '__main__':
    main()
