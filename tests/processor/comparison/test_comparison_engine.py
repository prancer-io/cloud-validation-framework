"""
Comprehensive tests for the comparison/rule engine.

Covers:
- get_operator_roperand parsing
- version_str conversion
- Comparator factory method
- ComparatorV01 format detection
- comparison_functions (equality, less_than, etc.)
- RuleInterpreter.get_field_value static method
- RuleInterpreter.rule_operands
- RuleInterpreter match/apply methods
- Result structure validation
- exclude_test_case logic
"""

import pytest


# ---------------------------------------------------------------------------
# Helpers – mock functions used across several test groups
# ---------------------------------------------------------------------------

def _mock_get_documents_empty(collection, query=None, dbname=None, sort=None, limit=10):
    return []


def _mock_get_documents_one(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "structure": "azure",
        "reference": "ref1",
        "source": "snap_source",
        "path": "/some/path",
        "collection": "microsoftcompute",
        "json": {
            "id": 124,
            "location": "eastus2",
            "name": "test-resource",
        },
        "snapshotId": "1",
        "timestamp": 1545908086831,
        "node": {"type": "Microsoft.Compute"},
        "region": "eastus2",
        "paths": ["/a/b/c"],
    }]


def _patch_common(monkeypatch):
    """Apply common monkeypatches for database / filesystem calls."""
    monkeypatch.setattr(
        'processor.comparison.interpreter.get_dbtests', lambda: 0
    )
    monkeypatch.setattr(
        'processor.comparison.interpreter.get_documents',
        _mock_get_documents_one,
    )
    monkeypatch.setattr(
        'processor.comparison.comparisonantlr.rule_interpreter.get_dbtests',
        lambda: 0,
    )
    monkeypatch.setattr(
        'processor.comparison.comparisonantlr.rule_interpreter.get_documents',
        _mock_get_documents_one,
    )


# ===================================================================
# 1. get_operator_roperand
# ===================================================================

class TestGetOperatorRoperand:

    @staticmethod
    def _call(value):
        from processor.comparison.interpreter import get_operator_roperand
        return get_operator_roperand(value)

    def test_eq_integer(self):
        is_not, op, roperand, extras = self._call("eq 10")
        assert is_not is False
        assert op == 'eq'
        assert roperand == 10
        assert extras is None

    def test_not_eq_integer(self):
        is_not, op, roperand, extras = self._call("not eq 10")
        assert is_not is True
        assert op == 'eq'
        assert roperand == 10

    def test_neq_maps_to_eq_with_not(self):
        is_not, op, roperand, extras = self._call("neq 10")
        assert is_not is True
        assert op == 'eq'
        assert roperand == 10

    def test_exist(self):
        is_not, op, roperand, extras = self._call("exist")
        assert is_not is False
        assert op == 'exist'
        assert roperand is None
        assert extras is None

    def test_not_exist(self):
        is_not, op, roperand, extras = self._call("not exist")
        assert is_not is True
        assert op == 'exist'

    def test_gt(self):
        is_not, op, roperand, extras = self._call("gt 5")
        assert is_not is False
        assert op == 'gt'
        assert roperand == 5

    def test_lt(self):
        is_not, op, roperand, extras = self._call("lt 100")
        assert op == 'lt'
        assert roperand == 100

    def test_le(self):
        is_not, op, roperand, extras = self._call("le 50")
        assert op == 'le'
        assert roperand == 50

    def test_ge(self):
        is_not, op, roperand, extras = self._call("ge 20")
        assert op == 'ge'
        assert roperand == 20

    def test_eq_quoted_string(self):
        is_not, op, roperand, extras = self._call("eq 'hello'")
        assert op == 'eq'
        assert roperand == 'hello'
        assert extras is None

    def test_eq_len_extra(self):
        is_not, op, roperand, extras = self._call("eq len(5)")
        assert op == 'eq'
        assert roperand == 5
        assert extras == ['len']

    def test_none_value(self):
        is_not, op, roperand, extras = self._call(None)
        assert op == 'exist'
        assert roperand is None

    def test_empty_string(self):
        is_not, op, roperand, extras = self._call("")
        assert op == 'exist'
        assert roperand is None


# ===================================================================
# 2. version_str
# ===================================================================

class TestVersionStr:

    @staticmethod
    def _call(version):
        from processor.comparison.interpreter import version_str
        return version_str(version)

    def test_zero_one(self):
        assert self._call("0.1") == "0_1"

    def test_zero_two(self):
        assert self._call("0.2") == "0_2"

    def test_none(self):
        assert self._call(None) is None


# ===================================================================
# 3. Comparator factory method
# ===================================================================

class TestComparatorFactory:

    def test_v01_created(self, monkeypatch):
        _patch_common(monkeypatch)
        from processor.comparison.interpreter import Comparator, ComparatorV01
        c = Comparator('0.1', 'ctr', 'db', {}, {'attribute': 'a', 'comparison': 'exist', 'testId': '1', 'snapshotId': '1'}, {}, {})
        assert isinstance(c.comparator, ComparatorV01)

    def test_v02_created(self, monkeypatch):
        _patch_common(monkeypatch)
        from processor.comparison.interpreter import Comparator, ComparatorV02
        c = Comparator('0.2', 'ctr', 'db', {}, {'attribute': 'a', 'comparison': 'exist', 'testId': '1', 'snapshotId': '1'}, {}, {})
        assert isinstance(c.comparator, ComparatorV02)

    def test_unknown_version_defaults_v01(self, monkeypatch):
        _patch_common(monkeypatch)
        from processor.comparison.interpreter import Comparator, ComparatorV01
        c = Comparator('9.9', 'ctr', 'db', {}, {'attribute': 'a', 'comparison': 'exist', 'testId': '1', 'snapshotId': '1'}, {}, {})
        assert isinstance(c.comparator, ComparatorV01)


# ===================================================================
# 4. ComparatorV01.__init__ format detection
# ===================================================================

class TestComparatorV01FormatDetection:

    def _make(self, monkeypatch, testcase):
        _patch_common(monkeypatch)
        from processor.comparison.interpreter import ComparatorV01
        return ComparatorV01('ctr', 'db', {}, testcase, {}, {})

    def test_attribute_comparison_v1(self, monkeypatch):
        from processor.comparison.interpreter import TESTCASEV1
        tc = {'attribute': 'location', 'comparison': 'exist', 'testId': '1', 'snapshotId': '1'}
        obj = self._make(monkeypatch, tc)
        assert obj.format == TESTCASEV1
        assert obj.type == 'prancer'

    def test_rego_type_v2(self, monkeypatch):
        from processor.comparison.interpreter import TESTCASEV2
        tc = {'type': 'rego', 'rule': 'input.x == true', 'testId': '1', 'snapshotId': ['1']}
        obj = self._make(monkeypatch, tc)
        assert obj.format == TESTCASEV2
        assert obj.type == 'rego'

    def test_python_type_v2(self, monkeypatch):
        from processor.comparison.interpreter import TESTCASEV2
        tc = {'type': 'python', 'rule': 'myrule.py', 'testId': '1', 'snapshotId': ['1']}
        obj = self._make(monkeypatch, tc)
        assert obj.format == TESTCASEV2
        assert obj.type == 'python'

    def test_rule_only_prancer(self, monkeypatch):
        from processor.comparison.interpreter import TESTCASEV2
        tc = {'rule': '{1}.location = "eastus2"', 'testId': '1', 'snapshotId': ['1']}
        obj = self._make(monkeypatch, tc)
        assert obj.format == TESTCASEV2
        assert obj.type == 'prancer'

    def test_no_match_format_none(self, monkeypatch):
        tc = {'testId': '1', 'snapshotId': '1'}
        obj = self._make(monkeypatch, tc)
        assert obj.format is None


# ===================================================================
# 5. comparison_functions – thorough tests
# ===================================================================

class TestEquality:

    @staticmethod
    def _call(*args, **kwargs):
        from processor.comparison.comparison_functions import equality
        return equality(*args, **kwargs)

    def test_match(self):
        assert self._call({'a': 10}, 'a', 10) is True

    def test_no_match(self):
        assert self._call({'a': 10}, 'a', 20) is False

    def test_type_mismatch_strict(self):
        # int 10 vs str '10' must fail because of type(value)==type(roperand)
        assert self._call({'a': 10}, 'a', '10') is False

    def test_is_not_flips_true(self):
        assert self._call({'a': 10}, 'a', 10, is_not=True) is False

    def test_is_not_flips_false(self):
        assert self._call({'a': 10}, 'a', 20, is_not=True) is True

    def test_extras_len(self):
        assert self._call({'a': [1, 2, 3]}, 'a', 3, extras=['len']) is True

    def test_extras_len_mismatch(self):
        assert self._call({'a': [1, 2]}, 'a', 3, extras=['len']) is False

    def test_missing_field(self):
        assert self._call({'a': 10}, 'b', 10) is False

    def test_nested_field(self):
        assert self._call({'a': {'b': 10}}, 'a.b', 10) is True


class TestLessThan:

    @staticmethod
    def _call(*args, **kwargs):
        from processor.comparison.comparison_functions import less_than
        return less_than(*args, **kwargs)

    def test_true(self):
        assert self._call({'a': 5}, 'a', 10) is True

    def test_false(self):
        assert self._call({'a': 10}, 'a', 5) is False

    def test_equal_is_false(self):
        assert self._call({'a': 5}, 'a', 5) is False

    def test_type_mismatch(self):
        assert self._call({'a': 5}, 'a', '10') is False

    def test_is_not(self):
        assert self._call({'a': 5}, 'a', 10, is_not=True) is False

    def test_missing_field(self):
        assert self._call({'a': 5}, 'b', 10) is False


class TestLessThanEqual:

    @staticmethod
    def _call(*args, **kwargs):
        from processor.comparison.comparison_functions import less_than_equal
        return less_than_equal(*args, **kwargs)

    def test_less(self):
        assert self._call({'a': 5}, 'a', 10) is True

    def test_equal(self):
        assert self._call({'a': 5}, 'a', 5) is True

    def test_greater(self):
        assert self._call({'a': 10}, 'a', 5) is False

    def test_is_not(self):
        assert self._call({'a': 5}, 'a', 10, is_not=True) is False


class TestGreaterThan:

    @staticmethod
    def _call(*args, **kwargs):
        from processor.comparison.comparison_functions import greater_than
        return greater_than(*args, **kwargs)

    def test_true(self):
        assert self._call({'a': 10}, 'a', 5) is True

    def test_false(self):
        assert self._call({'a': 5}, 'a', 10) is False

    def test_equal_is_false(self):
        assert self._call({'a': 5}, 'a', 5) is False

    def test_is_not(self):
        assert self._call({'a': 10}, 'a', 5, is_not=True) is False


class TestGreaterThanEqual:

    @staticmethod
    def _call(*args, **kwargs):
        from processor.comparison.comparison_functions import greater_than_equal
        return greater_than_equal(*args, **kwargs)

    def test_greater(self):
        assert self._call({'a': 10}, 'a', 5) is True

    def test_equal(self):
        assert self._call({'a': 5}, 'a', 5) is True

    def test_less(self):
        assert self._call({'a': 5}, 'a', 10) is False

    def test_is_not(self):
        assert self._call({'a': 10}, 'a', 5, is_not=True) is False


class TestExists:

    @staticmethod
    def _call(*args, **kwargs):
        from processor.comparison.comparison_functions import exists
        return exists(*args, **kwargs)

    def test_field_exists(self):
        assert self._call({'a': 10}, 'a', None) is True

    def test_field_missing(self):
        assert self._call({'a': 10}, 'b', None) is False

    def test_is_not_flips(self):
        assert self._call({'a': 10}, 'a', None, is_not=True) is False

    def test_nested_field(self):
        assert self._call({'a': {'b': 1}}, 'a.b', None) is True

    def test_nested_field_missing(self):
        assert self._call({'a': {'b': 1}}, 'a.c', None) is False


class TestApplyExtras:

    @staticmethod
    def _call(value, extras):
        from processor.comparison.comparison_functions import apply_extras
        return apply_extras(value, extras)

    def test_len_list(self):
        assert self._call([1, 2, 3], ['len']) == 3

    def test_len_string(self):
        assert self._call('hello', ['len']) == 5

    def test_len_no_len_attr(self):
        assert self._call(5, ['len']) == 0


# ===================================================================
# 6. RuleInterpreter.get_field_value (static)
# ===================================================================

class TestRuleInterpreterGetFieldValue:

    @staticmethod
    def _call(data, param):
        from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter
        return RuleInterpreter.get_field_value(data, param)

    def test_simple(self):
        assert self._call({'a': 1}, '.a') == 1

    def test_nested(self):
        assert self._call({'a': {'b': {'c': 3}}}, '.a.b.c') == 3

    def test_array_index(self):
        assert self._call({'a': [10, 20, 30]}, '.a[1]') == 20

    def test_array_filter(self):
        data = {'items': [{'name': 'x', 'val': 1}, {'name': 'y', 'val': 2}]}
        result = self._call(data, ".items[name='y']")
        assert result == {'name': 'y', 'val': 2}

    def test_wildcard(self):
        data = {'items': [{'a': 1}, {'a': 2}]}
        result = self._call(data, '.items[*]')
        assert result == [{'a': 1}, {'a': 2}]

    def test_missing_field(self):
        assert self._call({'a': 1}, '.b') is None

    def test_trailing_dot_removal(self):
        assert self._call({'a': 1}, '.a.') == 1

    def test_leading_dot_removal(self):
        assert self._call({'a': 1}, '.a') == 1

    def test_trailing_bracket_removal(self):
        # trailing [] is stripped before evaluation
        assert self._call({'a': [10, 20]}, '.a[]') == [10, 20]

    def test_none_data(self):
        assert self._call(None, '.a') is None

    def test_empty_parameter(self):
        assert self._call({'a': 1}, '') is None


# ===================================================================
# 7. RuleInterpreter.rule_operands
# ===================================================================

class TestRuleOperands:

    @staticmethod
    def _make(children):
        from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter
        # Provide minimal kwargs so __init__ does not fail
        return RuleInterpreter(children, dbname='db', snapshots={}, container='ctr')

    def test_eq_split(self):
        ri = self._make(["{1}.a", "=", "'hello'"])
        assert ri.lhs_operand == ["{1}.a"]
        assert ri.op == "="
        assert ri.rhs_operand == ["'hello'"]

    def test_neq_split(self):
        ri = self._make(["{1}.a", "!=", "10"])
        assert ri.lhs_operand == ["{1}.a"]
        assert ri.op == "!="
        assert ri.rhs_operand == ["10"]

    def test_defaults_single_child(self):
        ri = self._make(["{1}.a"])
        assert ri.lhs_operand == ["{1}.a"]
        assert ri.op == "="
        assert ri.rhs_operand == ["True"]

    def test_exist_method_single(self):
        ri = self._make(["exist({1}.a)"])
        assert ri.lhs_operand == ["exist({1}.a)"]
        assert ri.op == "="
        assert ri.rhs_operand == ["True"]

    def test_gt_split(self):
        ri = self._make(["{1}.count", ">", "5"])
        assert ri.op == ">"

    def test_lte_split(self):
        ri = self._make(["{1}.count", "<=", "5"])
        assert ri.op == "<="


# ===================================================================
# 8. RuleInterpreter match methods
# ===================================================================

class TestRuleInterpreterMatchMethods:

    @staticmethod
    def _make():
        from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter
        return RuleInterpreter([], dbname='db', snapshots={}, container='ctr')

    def test_match_number_int(self):
        ri = self._make()
        import re
        m = re.match(r'^(\d+)(\.\d+)?$', '123')
        assert ri.match_number('123', m) == 123

    def test_match_number_float(self):
        ri = self._make()
        import re
        m = re.match(r'^(\d+)(\.\d+)?$', '12.5')
        assert ri.match_number('12.5', m) == 12.5

    def test_match_boolean_true(self):
        ri = self._make()
        assert ri.match_boolean('true', None) is True

    def test_match_boolean_false(self):
        ri = self._make()
        assert ri.match_boolean('false', None) is False

    def test_match_string(self):
        ri = self._make()
        assert ri.match_string("'hello'", None) == 'hello'

    def test_match_string_no_quotes(self):
        ri = self._make()
        assert ri.match_string("world", None) == 'world'

    def test_match_array_string(self):
        ri = self._make()
        result = ri.match_array_string("['a','b','c']", None)
        assert result == ['a', 'b', 'c']

    def test_match_method_exist(self):
        ri = self._make()
        method, args = ri.match_method("exist({1}.a)")
        assert method == "exist"
        assert args == "{1}.a"

    def test_match_method_count(self):
        ri = self._make()
        method, args = ri.match_method("count({1}.items)")
        assert method == "count"
        assert args == "{1}.items"

    def test_match_method_no_parens(self):
        ri = self._make()
        method, args = ri.match_method("{1}.a")
        assert method is None
        assert args == "{1}.a"

    def test_is_method_true(self):
        ri = self._make()
        assert ri.is_method("exist({1}.a)") is True

    def test_is_method_false(self):
        ri = self._make()
        assert ri.is_method("{1}.a") is False


# ===================================================================
# 9. RuleInterpreter.apply_method
# ===================================================================

class TestRuleInterpreterApplyMethod:

    @staticmethod
    def _make():
        from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter
        return RuleInterpreter([], dbname='db', snapshots={}, container='ctr')

    def test_exist_present(self):
        ri = self._make()
        assert ri.apply_method('exist', {'a': 1}, '{1}.a') is True

    def test_exist_none(self):
        ri = self._make()
        assert ri.apply_method('exist', None, '{1}.a') is False

    def test_exists_alias(self):
        ri = self._make()
        assert ri.apply_method('exists', {'a': 1}, '{1}.a') is True

    def test_count_list(self):
        ri = self._make()
        assert ri.apply_method('count', [1, 2, 3], '{1}.items') == 3

    def test_count_none(self):
        ri = self._make()
        assert ri.apply_method('count', None, '{1}.items') == 0

    def test_contain_sets_op(self):
        ri = self._make()
        ri.apply_method('contain', [1, 2], '{1}.items')
        assert ri.op == 'in'

    def test_contains_sets_op(self):
        ri = self._make()
        ri.apply_method('contains', [1, 2], '{1}.items')
        assert ri.op == 'in'


# ===================================================================
# 10. Result structure validation
# ===================================================================

class TestResultStructure:

    def test_unsupported_format_returns_skipped(self, monkeypatch):
        _patch_common(monkeypatch)
        from processor.comparison.interpreter import ComparatorV01
        tc = {'testId': '1', 'snapshotId': '1'}
        obj = ComparatorV01('ctr', 'db', {}, tc, {}, {})
        # format is None -> unsupported
        results = obj.validate()
        assert len(results) == 1
        assert results[0]['result'] == 'skipped'
        assert 'reason' in results[0]
        assert results[0]['reason'] == 'Unsupported testcase format'

    def test_testcasev1_result_has_snapshots(self, monkeypatch):
        _patch_common(monkeypatch)
        # For TESTCASEV1, validate fetches from DB. Mock get_documents to return a doc.
        monkeypatch.setattr(
            'processor.comparison.interpreter.get_documents',
            _mock_get_documents_one,
        )
        monkeypatch.setattr(
            'processor.comparison.interpreter.get_dbtests', lambda: 1
        )
        from processor.comparison.interpreter import ComparatorV01
        tc = {
            'testId': '1',
            'snapshotId': '1',
            'attribute': 'location',
            'comparison': 'exist',
        }
        obj = ComparatorV01('ctr', 'db', {}, tc, {}, {})
        results = obj.validate()
        assert len(results) == 1
        assert results[0]['result'] in ('passed', 'failed', 'skipped')
        if results[0]['result'] == 'passed':
            assert 'snapshots' in results[0]
            snap = results[0]['snapshots'][0]
            for key in ('id', 'structure', 'reference', 'source', 'collection'):
                assert key in snap

    def test_result_values_are_valid_strings(self, monkeypatch):
        _patch_common(monkeypatch)
        monkeypatch.setattr(
            'processor.comparison.interpreter.get_dbtests', lambda: 1
        )
        from processor.comparison.interpreter import ComparatorV01
        tc = {
            'testId': '1',
            'snapshotId': '1',
            'attribute': 'location',
            'comparison': 'eq \'eastus2\'',
        }
        obj = ComparatorV01('ctr', 'db', {}, tc, {}, {})
        results = obj.validate()
        for r in results:
            assert r['result'] in ('passed', 'failed', 'skipped')


# ===================================================================
# 11. exclude_test_case logic
# ===================================================================

class TestExcludeTestCase:

    def _make(self, monkeypatch, excludedTestIds=None, includeTests=None, testcase=None):
        _patch_common(monkeypatch)
        from processor.comparison.interpreter import ComparatorV01
        tc = testcase or {'testId': '1', 'snapshotId': '1'}
        obj = ComparatorV01(
            'ctr', 'db', {},
            tc,
            excludedTestIds or {},
            includeTests or {},
        )
        return obj

    def test_in_include_tests_not_excluded(self, monkeypatch):
        obj = self._make(monkeypatch, includeTests={'MT1': True})
        doc = {'paths': ['/a/b']}
        assert obj.exclude_test_case(doc, 'MT1', isMasterTest=True) is False

    def test_in_excluded_and_path_matches(self, monkeypatch):
        obj = self._make(monkeypatch, excludedTestIds={'MT1': ['/a/b']})
        doc = {'paths': ['/a/b']}
        assert obj.exclude_test_case(doc, 'MT1', isMasterTest=True) is True

    def test_in_excluded_but_path_no_match(self, monkeypatch):
        obj = self._make(monkeypatch, excludedTestIds={'MT1': ['/x/y']})
        doc = {'paths': ['/a/b']}
        assert obj.exclude_test_case(doc, 'MT1', isMasterTest=True) is False

    def test_not_master_test_not_excluded(self, monkeypatch):
        obj = self._make(monkeypatch)
        doc = {'paths': ['/a/b']}
        # isMasterTest=False -> always False
        assert obj.exclude_test_case(doc, 'T1', isMasterTest=False) is False

    def test_not_in_either_for_master(self, monkeypatch):
        obj = self._make(monkeypatch)
        doc = {'paths': ['/a/b']}
        # testId not in includeTests or excludedTestIds, no evals
        assert obj.exclude_test_case(doc, 'MT_UNKNOWN', isMasterTest=True) is False

    def test_evals_include_check(self, monkeypatch):
        tc = {
            'testId': '1',
            'snapshotId': '1',
            'evals': [{'id': 'E1', 'eval': 'data.rule.r1'}],
        }
        obj = self._make(monkeypatch, includeTests={'E1': True}, testcase=tc)
        doc = {'paths': ['/a/b']}
        # E1 is in includeTests -> found=True -> not excluded
        assert obj.exclude_test_case(doc, 'MT_OTHER', isMasterTest=True) is False

    def test_evals_excluded_path_match(self, monkeypatch):
        tc = {
            'testId': '1',
            'snapshotId': '1',
            'evals': [{'id': 'E1', 'eval': 'data.rule.r1'}],
        }
        obj = self._make(
            monkeypatch,
            excludedTestIds={'E1': ['/a/b']},
            testcase=tc,
        )
        doc = {'paths': ['/a/b']}
        assert obj.exclude_test_case(doc, 'MT_OTHER', isMasterTest=True) is True


# ===================================================================
# Extra: compare_types basics (used by RuleInterpreter.compare)
# ===================================================================

class TestCompareTypes:

    def test_compare_int_eq(self):
        from processor.comparison.comparisonantlr.compare_types import compare_int, EQ
        assert compare_int(10, 10, EQ) is True

    def test_compare_int_neq(self):
        from processor.comparison.comparisonantlr.compare_types import compare_int, NEQ
        assert compare_int(10, 20, NEQ) is True

    def test_compare_str_eq(self):
        from processor.comparison.comparisonantlr.compare_types import compare_str, EQ
        assert compare_str('a', 'a', EQ) is True

    def test_compare_boolean_eq(self):
        from processor.comparison.comparisonantlr.compare_types import compare_boolean, EQ
        assert compare_boolean(True, True, EQ) is True

    def test_compare_in_present(self):
        from processor.comparison.comparisonantlr.compare_types import compare_in
        assert compare_in(['a', 'b', 'c'], 'b', 'in') is True

    def test_compare_in_absent(self):
        from processor.comparison.comparisonantlr.compare_types import compare_in
        assert compare_in(['a', 'b'], 'z', 'in') is False
