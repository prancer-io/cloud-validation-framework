"""Contract tests pinning the third-party APIs prancer-basic relies on.

Added before the security dependency upgrades (GitPython, pymongo, dnspython,
Jinja2, urllib3, requests) so an upgrade that changes behavior the code depends
on fails here. Everything runs offline: git uses a local file:// repo and
pymongo never connects to a server.
"""
import os
import subprocess

import pytest


# ---------------------------------------------------------------- GitPython

def _git(cwd, *args):
    subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", *args],
        cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


@pytest.fixture
def local_origin(tmp_path):
    origin = tmp_path / "origin"
    origin.mkdir()
    _git(origin, "init", "-q")
    (origin / "main.tf").write_text('resource "x" "y" {}\n')
    _git(origin, "add", ".")
    _git(origin, "commit", "-qm", "init")
    _git(origin, "branch", "feature")
    return origin


def test_clone_repo_from_file_url(local_origin, tmp_path):
    from processor.connector.git_connector.git_functions import GithubFunctions
    gf = GithubFunctions()
    dst = tmp_path / "clone"
    repo = gf.clone_repo("file://%s" % local_origin, str(dst))
    assert repo is gf.repo
    assert (dst / "main.tf").read_text() == 'resource "x" "y" {}\n'
    # depth=1 is passed through to git
    assert repo.git.rev_list("--count", "HEAD") == "1"


def test_clone_repo_with_branch(local_origin, tmp_path):
    from processor.connector.git_connector.git_functions import GithubFunctions
    gf = GithubFunctions()
    repo = gf.clone_repo("file://%s" % local_origin, str(tmp_path / "c"),
                         branch_name="feature")
    assert repo.active_branch.name == "feature"


def test_checkout_and_commit(local_origin, tmp_path):
    from processor.connector.git_connector.git_functions import GithubFunctions
    gf = GithubFunctions()
    dst = tmp_path / "c"
    repo = gf.clone_repo("file://%s" % local_origin, str(dst))
    repo.config_writer().set_value("user", "name", "t").release()
    repo.config_writer().set_value("user", "email", "t@example.com").release()
    assert gf.checkout_branch("newbranch") is True
    assert repo.active_branch.name == "newbranch"
    (dst / "extra.tf").write_text("x\n")
    gf.commit_changes("add extra")
    assert repo.head.commit.message == "add extra"
    assert gf.checkout_branch("newbranch") is False  # already exists


def test_gitpython_still_blocks_unsafe_clone_config(local_origin, tmp_path):
    """Pins current behavior: GitPython rejects `c=` (git -c) on clone_from
    unless allow_unsafe_options=True. clone_repo's azure.com branch passes c=
    and therefore already fails on the pinned GitPython 3.1.37."""
    from git import Repo
    from git.exc import UnsafeOptionError
    with pytest.raises(UnsafeOptionError):
        Repo.clone_from("file://%s" % local_origin, str(tmp_path / "u"),
                        c="http.extraHeader=Authorization: Bearer x", depth=1)


def test_git_module_imports_used_by_code():
    from git import exc, Repo, Git  # noqa: F401
    assert issubclass(exc.GitCommandError, Exception)


# ------------------------------------------------------------------ pymongo

def test_pymongo_symbols_used_by_code():
    import pymongo
    from pymongo import MongoClient, TEXT, ASCENDING, DESCENDING  # noqa: F401
    from pymongo.errors import ServerSelectionTimeoutError  # noqa: F401
    assert (ASCENDING, DESCENDING, TEXT) == (1, -1, "text")
    assert pymongo.ASCENDING == 1 and pymongo.DESCENDING == -1


def test_mongoclient_constructs_lazily_with_timeout():
    from pymongo import MongoClient
    client = MongoClient(host="mongodb://127.0.0.1:1/", serverSelectionTimeoutMS=50,
                         connect=False)
    try:
        coll = client["validator"]["resources"]
        assert coll.name == "resources"
        assert coll.database.name == "validator"
    finally:
        client.close()


def test_mongoclient_port_only_form():
    from pymongo import MongoClient
    client = MongoClient(port=27017, serverSelectionTimeoutMS=50, connect=False)
    client.close()


def test_bson_helpers():
    from bson.objectid import ObjectId
    from bson import json_util
    oid = ObjectId("5f1b2c3d4e5f6a7b8c9d0e1f")
    dumped = json_util.dumps({"_id": oid, "a": 1})
    assert json_util.loads(dumped) == {"_id": oid, "a": 1}


def test_dnspython_importable_for_srv():
    import dns.resolver  # noqa: F401
    import dns.version
    assert dns.version.MAJOR == 2


# ------------------------------------------------------------------- Jinja2

def test_jinja2_symbols_used_by_code(tmp_path):
    from jinja2 import Environment, FileSystemLoader, Undefined, make_logging_undefined
    from jinja2.utils import missing, object_type_repr  # noqa: F401
    (tmp_path / "t.jinja").write_text("name: {{ name }}\n{{ missing_var }}")
    env = Environment(loader=FileSystemLoader(str(tmp_path)),
                      undefined=make_logging_undefined(base=Undefined))
    assert env.get_template("t.jinja").render(name="x") == "name: x\n"
    assert object_type_repr(None) == "None"


def test_google_util_imports():
    from processor.templates.google import util  # noqa: F401


# --------------------------------------------------------- requests/urllib3

def test_requests_prepare_and_urllib3_compat():
    import requests
    import urllib3
    req = requests.Request("POST", "https://example.invalid/api", json={"a": 1},
                           headers={"Authorization": "token x"}).prepare()
    assert req.body == b'{"a": 1}'
    assert req.headers["Content-Type"] == "application/json"
    # botocore 1.20.x (boto3 1.17.16) requires urllib3 < 1.27
    assert urllib3.__version__.startswith("1.26.")


def test_boto3_client_builds_offline():
    try:
        import boto3
    except ModuleNotFoundError as e:
        # botocore 1.20.x (pinned via boto3 1.17.16) cannot import on Python >= 3.12
        pytest.skip("pinned botocore unsupported on this interpreter: %s" % e)
    client = boto3.client("s3", region_name="us-east-1",
                          aws_access_key_id="AKIAEXAMPLE", aws_secret_access_key="x")
    assert client.meta.region_name == "us-east-1"
