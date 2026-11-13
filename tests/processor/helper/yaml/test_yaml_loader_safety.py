"""
Pin the behaviour of processor.helper.yaml.yaml_utils across the switch from
yaml FullLoader to SafeLoader (Gadriel CODE-W1-L3-016 / CODE-W1-L3-029).

* Behaviour tests: normal, multi-document, invalid and CloudFormation-tag
  input for yaml_from_string, yaml_from_file, valid_yaml,
  multiple_yaml_from_file and is_multiple_yaml_file. These must pass both
  before and after the change.
* Equivalence test: every .yaml/.yml file in the repository loads to the
  identical result (or fails with the same exception type) under FullLoader
  and SafeLoader.
* Safety tests: `!!python/*` tags (only constructed by FullLoader) are rejected.
"""
import datetime
import os

import pytest
import yaml
from yaml.loader import FullLoader, SafeLoader

from processor.helper.yaml.yaml_utils import (
    yaml_from_string, yaml_from_file, valid_yaml, multiple_yaml_from_file,
    is_multiple_yaml_file, save_yaml_to_file)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

NORMAL_YAML = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels: &labels
    app: web
spec:
  replicas: 3
  ratio: 0.5
  enabled: true
  nothing: null
  tilde: ~
  created: 2021-01-02
  stamp: 2021-01-02 03:04:05
  octal: 0o17
  hex: 0x1f
  quoted: "123"
  selector:
    matchLabels: *labels
  merged:
    <<: *labels
    extra: 1
  ports: [80, 443]
  blob: !!binary aGVsbG8=
  members: !!set {a, b}
"""

NORMAL_EXPECTED = {
    'apiVersion': 'apps/v1',
    'kind': 'Deployment',
    'metadata': {'name': 'web', 'labels': {'app': 'web'}},
    'spec': {
        'replicas': 3,
        'ratio': 0.5,
        'enabled': True,
        'nothing': None,
        'tilde': None,
        'created': datetime.date(2021, 1, 2),
        'stamp': datetime.datetime(2021, 1, 2, 3, 4, 5),
        'octal': '0o17',
        'hex': 31,
        'quoted': '123',
        'selector': {'matchLabels': {'app': 'web'}},
        'merged': {'app': 'web', 'extra': 1},
        'ports': [80, 443],
        'blob': b'hello',
        'members': {'a', 'b'},
    },
}

MULTI_YAML = """\
---
# Source: chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: svc
---
# Source: chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dep
---
"""

MULTI_EXPECTED = [
    {'apiVersion': 'v1', 'kind': 'Service', 'metadata': {'name': 'svc'}},
    {'apiVersion': 'apps/v1', 'kind': 'Deployment', 'metadata': {'name': 'dep'}},
    None,
]

INVALID_YAML = "hello: ][\n  - : :\n"

CFN_YAML = """\
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketParam
      Arn: !GetAtt Other.Arn
"""

PYTHON_TAG_DOCS = [
    "a: !!python/tuple [1, 2]\n",
    "a: !!python/name:os.system\n",
    "a: !!python/complex 1+2j\n",
]


def _write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text)
    return str(path)


# ---------------------------------------------------------------- yaml_from_string
def test_yaml_from_string_normal():
    assert yaml_from_string(NORMAL_YAML) == NORMAL_EXPECTED


def test_yaml_from_string_list_and_scalar():
    assert yaml_from_string("- a\n- 1\n") == ['a', 1]
    assert yaml_from_string("abcd") == 'abcd'
    assert yaml_from_string("") is None


def test_yaml_from_string_multi_doc_returns_none():
    assert yaml_from_string(MULTI_YAML) is None


def test_yaml_from_string_invalid_returns_none():
    assert yaml_from_string(INVALID_YAML) is None
    assert yaml_from_string(None) is None


def test_yaml_from_string_cfn_tags_return_none():
    assert yaml_from_string(CFN_YAML) is None


# ---------------------------------------------------------------- yaml_from_file
def test_yaml_from_file_normal(tmp_path):
    path = _write(tmp_path, 'n.yaml', NORMAL_YAML)
    assert yaml_from_file(path) == NORMAL_EXPECTED


@pytest.mark.parametrize('loader', [FullLoader, SafeLoader])
def test_yaml_from_file_explicit_loader(tmp_path, loader):
    path = _write(tmp_path, 'n.yaml', NORMAL_YAML)
    assert yaml_from_file(path, loader=loader) == NORMAL_EXPECTED


def test_yaml_from_file_multi_invalid_cfn_missing(tmp_path):
    assert yaml_from_file(_write(tmp_path, 'm.yaml', MULTI_YAML)) is None
    assert yaml_from_file(_write(tmp_path, 'i.yaml', INVALID_YAML)) is None
    assert yaml_from_file(_write(tmp_path, 'c.yaml', CFN_YAML)) is None
    assert yaml_from_file(str(tmp_path / 'missing.yaml')) is None
    assert yaml_from_file(None) is None


# ---------------------------------------------------------------- valid_yaml
def test_valid_yaml():
    assert valid_yaml(NORMAL_YAML) is True
    assert valid_yaml("- a\n- b\n") is False
    assert valid_yaml("abcd") is False
    assert valid_yaml(MULTI_YAML) is False
    assert valid_yaml(INVALID_YAML) is False
    assert valid_yaml(CFN_YAML) is False
    assert valid_yaml(None) is False


# ---------------------------------------------------------------- multiple_yaml_from_file
@pytest.mark.parametrize('loader', [None, FullLoader, SafeLoader])
def test_multiple_yaml_from_file(tmp_path, loader):
    assert multiple_yaml_from_file(_write(tmp_path, 'm.yaml', MULTI_YAML), loader=loader) == MULTI_EXPECTED
    assert multiple_yaml_from_file(_write(tmp_path, 'n.yaml', NORMAL_YAML), loader=loader) == [NORMAL_EXPECTED]
    assert multiple_yaml_from_file(_write(tmp_path, 'i.yaml', INVALID_YAML), loader=loader) is None
    assert multiple_yaml_from_file(_write(tmp_path, 'c.yaml', CFN_YAML), loader=loader) is None
    assert multiple_yaml_from_file(str(tmp_path / 'missing.yaml'), loader=loader) is None


# ---------------------------------------------------------------- is_multiple_yaml_file
def test_is_multiple_yaml_file(tmp_path):
    assert is_multiple_yaml_file(_write(tmp_path, 'm.yaml', MULTI_YAML)) is True
    assert is_multiple_yaml_file(_write(tmp_path, 'n.yaml', NORMAL_YAML)) is False
    assert is_multiple_yaml_file(_write(tmp_path, 'i.yaml', INVALID_YAML)) is False
    assert is_multiple_yaml_file(_write(tmp_path, 'c.yaml', CFN_YAML)) is False
    assert is_multiple_yaml_file(str(tmp_path / 'missing.yaml')) is False


def test_split_and_reload_round_trip(tmp_path):
    """Mirror BaseTemplateProcessor.break_multiple_yaml_file: split a rendered
    helm/multi-doc file, save each doc with save_yaml_to_file, reload it."""
    docs = multiple_yaml_from_file(_write(tmp_path, 'm.yaml', MULTI_YAML))
    for index, doc in enumerate(docs):
        out = str(tmp_path / ('m_multiple_yaml_%d.yaml' % index))
        save_yaml_to_file(doc, out)
        assert yaml_from_file(out) == doc
    out = str(tmp_path / 'normal_round_trip.yaml')
    save_yaml_to_file(NORMAL_EXPECTED, out)
    assert yaml_from_file(out) == NORMAL_EXPECTED


# ---------------------------------------------------------------- FullLoader == SafeLoader on repo files
def _repo_yaml_files():
    found = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', '__pycache__')]
        for name in filenames:
            if name.lower().endswith(('.yaml', '.yml')):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def _load(text, loader, multi):
    try:
        if multi:
            return ('ok', repr(list(yaml.load_all(text, Loader=loader))))
        return ('ok', repr(yaml.load(text, Loader=loader)))
    except Exception as ex:
        return ('error', type(ex).__name__)


def test_repo_yaml_files_found():
    assert len(_repo_yaml_files()) >= 10


@pytest.mark.parametrize('path', _repo_yaml_files(),
                         ids=lambda p: os.path.relpath(p, REPO_ROOT))
def test_full_and_safe_loader_equivalent_on_repo_yaml(path):
    with open(path, encoding='utf-8') as handle:
        text = handle.read()
    if '!!python/' in text:
        pytest.skip('contains python tags (FullLoader-only by design)')
    for multi in (False, True):
        assert _load(text, FullLoader, multi) == _load(text, SafeLoader, multi)


# ---------------------------------------------------------------- python tags are rejected
@pytest.mark.parametrize('text', PYTHON_TAG_DOCS)
def test_python_tags_rejected(tmp_path, text):
    path = _write(tmp_path, 'p.yaml', text)
    assert yaml_from_string(text) is None
    assert valid_yaml(text) is False
    assert yaml_from_file(path) is None
    assert multiple_yaml_from_file(path) is None
    assert is_multiple_yaml_file(path) is False
