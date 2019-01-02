""" Tests for validation"""
import re
from unittest.mock import MagicMock, Mock


def mock_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "_id": "5c24af787456217c485ad1e6",
        "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
        "collection": "microsoftcompute",
        "json": {
            "id": 124,
            "location": "eastus2",
            "name": "mno-nonprod-shared-cet-eastus2-tab-as03"
        },
        "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
        "snapshotId": 1,
        "timestamp": 1545908086831
    }]

def mock_get_multiple_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "_id": "5c24af787456217c485ad1e6",
        "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
        "collection": "microsoftcompute",
        "json": [{
            "id": 124,
            "location": "eastus2",
            "name": "mno-nonprod-shared-cet-eastus2-tab-as03",
            "addresses":[1,2,3,4]
        },
            {
                "id": 125,
                "location": "eastus",
                "name": "mno-nonprod-shared-cet-eastus2-tab-as04"
            }
        ],
        "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
        "snapshotId": 1,
        "timestamp": 1545908086831
    }]


def test_compare_none():
    from processor.comparison.comparisonantlr.compare_types import compare_none, EQ
    assert True == compare_none(None, None, EQ)
    assert False == compare_none('', None, EQ)
    assert False == compare_none(None, '', EQ)


def test_compare_int():
    from processor.comparison.comparisonantlr.compare_types import compare_int, EQ
    assert True == compare_int(1, 1, EQ)
    assert False == compare_int(None, None, EQ)
    assert False == compare_int('', None, EQ)
    assert False == compare_int(None, '', EQ)


def test_compare_float():
    from processor.comparison.comparisonantlr.compare_types import compare_float, EQ
    assert True == compare_float(1.00001, 1.00001, EQ)
    assert False == compare_float(1.00001, 1.000001, EQ)
    assert False == compare_float(1.00001, None, EQ)


def test_compare_boolean():
    from processor.comparison.comparisonantlr.compare_types import compare_boolean, EQ, NEQ
    assert True == compare_boolean(True, True, EQ)
    assert False == compare_boolean(True, False, EQ)
    assert True == compare_boolean(True, False, NEQ)
    assert True == compare_boolean(False, True, NEQ)
    assert False == compare_boolean(None, False, EQ)


def test_compare_str():
    from processor.comparison.comparisonantlr.compare_types import compare_str, EQ
    assert True == compare_str('', '', EQ)
    assert False == compare_str(None, '', EQ)


def test_compare_list():
    from processor.comparison.comparisonantlr.compare_types import compare_list, EQ
    assert True == compare_list([], [], EQ)
    assert False == compare_list(None, [], EQ)


def test_compare_dict():
    from processor.comparison.comparisonantlr.compare_types import compare_dict, EQ
    assert True == compare_dict({}, {}, EQ)
    assert False == compare_dict(None, {}, EQ)


def test_test_comparator(create_temp_dir):
    from processor.comparison.comparisonantlr.test_comparator import main
    rules = [
        "count({1}.firewall.rules[] + {2}.firewall.rules[]) = 13",
        "{1}.firewall.rules['name' = 'rule1'].port = {2}.firewall.rules['name' = 'rule1'].port",
        "count({1}.firewall.rules[]) = count({2}.firewall.rules[])",
        "count(count({1}.firewall.rules[]) + count({1}.firewall.rules[])) = 13",
        "exist({1}.location)",
        "exist({1}.firewall.location)",
        "exist({1}.firewall.rules[])",
        "count({1}.firewall.rules[]) != 13",
        "count({1}.firewall.rules[]) = 13",
        "{1}.firewall.port = 443",
        "{1}.location = 'eastus2'",
        "exist({1}.location) = FAlSE",
        "{1}.firewall.port = 443",
        "{1}.firewall.rules['name' = 'rule1'].port = 443",
        "{1}.firewall.port = {2}.firewall.port",
        "{1}.firewall.rules[0].port = {2}.firewall.port",
        "exist({1}[0].location)",
        "exist({1}['name' = 'abc'])",
        "{1}.firewall.rules['name' = 'abc'].port = {2}.firewall.port",
        "{1}.firewall.rules['name' = 'abc'].ports[2].port = {2}.firewall.port",
        "{1}.firewall.cost = 443.25"
    ]
    newpath = create_temp_dir()
    input = '%s/input.txt' % newpath
    with open(input, 'w') as testfile:
        testfile.write('\n'.join(rules))
    assert True == main(['', input])
    assert False == main(['', ''])


def test_is_method():
    from processor.comparison.interpreter import RuleInterpreter
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "count", "(", "{2}.firewall.rules[]",")"]
    otherdata = {}
    r_i = RuleInterpreter(children, **otherdata)
    assert  True == r_i.is_method(''.join(r_i.lhs_operand))
    assert True == r_i.is_method(''.join(r_i.rhs_operand))


def test_match_method():
    from processor.comparison.interpreter import RuleInterpreter
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "count", "(", "{2}.firewall.rules[]",")"]
    otherdata = {}
    r_i = RuleInterpreter(children, **otherdata)
    method, method_args = r_i.match_method(''.join(r_i.lhs_operand))
    assert method == 'count'
    assert method_args == "{1}.firewall.rules[]"


def test_match_number(monkeypatch):
    monkeypatch.setattr('processor.comparison.comparisonantlr.rule_interpreter.get_documents', mock_get_documents)
    from processor.comparison.interpreter import RuleInterpreter
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "22"]
    otherdata = {'dbname': 'validator', 'snapshots': {}}
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.rhs_operand)
    m = re.match(r'(\d+)(\.\d+)?', inval, re.I)
    val = r_i.match_number(inval, m)
    assert type(val) is int
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "22.45"]
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.rhs_operand)
    m = re.match(r'(\d+)(\.\d+)?', inval, re.I)
    val = r_i.match_number(inval, m)
    assert type(val) is float
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "False"]
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.rhs_operand)
    m = re.match(r'true|false', inval, re.I)
    val = r_i.match_boolean(inval, m)
    assert type(val) is bool
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "'eastus2'"]
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.rhs_operand)
    m = re.match(r'\'.*\'', inval, re.I)
    val = r_i.match_string(inval, m)
    assert type(val) is str
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "['eastus2', 'abc']"]
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.rhs_operand)
    m = re.match(r'\[.*\]', inval, re.I)
    val = r_i.match_array_string(inval, m)
    assert type(val) is list
    children = ["count", "(", "{1}.firewall.rules[]", ")", "=", "{'eastus2': 'abc'}"]
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.rhs_operand)
    m = re.match(r'\{.*\}', inval, re.I)
    val = r_i.match_dictionary_string(inval, m)
    assert type(val) is dict
    # children = ["exist", "(", "{1}.location", ")", "=", "'eastus2'"]
    children = ["{1}.location", "=", "'eastus2'"]
    r_i = RuleInterpreter(children, **otherdata)
    inval = ''.join(r_i.lhs_operand)
    val = r_i.get_value(r_i.lhs_operand)
    assert type(val) is str
    assert val == 'eastus2'


def test_match_array_attribute(monkeypatch):
    monkeypatch.setattr('processor.comparison.comparisonantlr.rule_interpreter.get_documents', mock_get_multiple_documents)
    from processor.comparison.interpreter import RuleInterpreter
    otherdata = {'dbname': 'validator', 'snapshots': {}}
    children = ["{1}[1].location", "=", "'eastus'"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.get_value(r_i.lhs_operand)
    assert type(val) is str
    assert val == 'eastus'
    children = ["{1}['name' = 'mno-nonprod-shared-cet-eastus2-tab-as04'].location", "=", "'eastus'"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.get_value(r_i.lhs_operand)
    assert type(val) is str
    assert val == 'eastus'
    children = ["exist", "(", "{1}['name' = 'mno-nonprod-shared-cet-eastus2-tab-as04'].location", ")"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.get_value(r_i.lhs_operand)
    assert type(val) is bool
    assert val == True


def test_compare(monkeypatch):
    monkeypatch.setattr('processor.comparison.comparisonantlr.rule_interpreter.get_documents', mock_get_multiple_documents)
    from processor.comparison.interpreter import RuleInterpreter
    otherdata = {'dbname': 'validator', 'snapshots': {}}
    children = ["{1}[1].location", "=", "'eastus'"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.compare()
    assert type(val) is bool
    assert val == True
    children = ["{1}['name' = 'mno-nonprod-shared-cet-eastus2-tab-as04'].location", "=", "False"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.compare()
    assert type(val) is bool
    assert val == False

def test_get_value(monkeypatch):
    monkeypatch.setattr('processor.comparison.comparisonantlr.rule_interpreter.get_documents',
                        mock_get_documents)
    from processor.comparison.interpreter import RuleInterpreter
    otherdata = {'dbname': 'validator', 'snapshots': {}}
    children = ["{1}.location", "+", "{1}.location", "=", "'eastus'"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.get_value(r_i.lhs_operand)
    assert type(val) is str
    assert val == 'eastus2eastus2'


def test_eval_expression(monkeypatch):
    monkeypatch.setattr('processor.comparison.comparisonantlr.rule_interpreter.get_documents',
                        mock_get_documents)
    from processor.comparison.interpreter import RuleInterpreter
    otherdata = {'dbname': 'validator', 'snapshots': {}}
    children = ["exist", "(", "{1}.location", ")"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.eval_expression(''.join(r_i.lhs_operand))
    assert type(val) is bool
    assert val == True
    children = ["exist", "(", "{1}.location1", ")", "=", "False"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.eval_expression(''.join(r_i.lhs_operand))
    assert type(val) is bool
    assert val == False
    children = ["count", "(", "{1}.location", ")", "=", "7"]
    r_i = RuleInterpreter(children, **otherdata)
    val = r_i.eval_expression(''.join(r_i.lhs_operand))
    assert type(val) is int
    assert val == 7

def test_get_field_value():
    from processor.comparison.interpreter import RuleInterpreter
    otherdata = {'dbname': 'validator', 'snapshots': {}}
    children = ["exist", "(", "{1}.location", ")"]
    r_i = RuleInterpreter(children, **otherdata)
    data = {'a': 1 , 'b': [{'c':'d'}, {'c': 'f'}]}
    val = RuleInterpreter.get_field_value(data, 'b[].c')
    assert val is None
    val = RuleInterpreter.get_field_value(data, 'b[2].c')
    assert val is None
    val = RuleInterpreter.get_field_value(data, 'b[2d].c')
    assert val is None
    data = {'a': 1, 'b': [{'c': 'd'}, {'c': 'f'}], 'c': {'d': 'e'}}
    val = RuleInterpreter.get_field_value(data, 'c[0].d')
    assert val is None
    val = RuleInterpreter.get_field_value(data, 'c.e')
    assert val is None