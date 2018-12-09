import pytest
import os.path
import tempfile
from processor.helper.comparison.comparison_functions import apply_extras, equality,\
    less_than, less_than_equal, greater_than, greater_than_equal, exists

extras = ['len']


def test_apply_extras():
    assert 0 == apply_extras('', extras)
    assert 0 == apply_extras(None, extras)
    assert 0 == apply_extras([], extras)
    assert 0 == apply_extras({}, extras)
    assert 4 == apply_extras('abcd', extras)
    assert 5 == apply_extras([1,2,3,4,5], extras)


def test_equality():
    data = {'a': 'b', 'c': 1, 'd': [1,2,3], 'e': {'h':1}}
    assert True == equality(data, 'a', 'b')
    assert True == equality(data, 'd', 3, extras=extras)
    assert True == equality(data, 'a', 'd', is_not=True, extras=extras)


def test_less_than():
    data = {'a': 'b', 'c': 4, 'd': [1,2,3], 'e': {'h':1}}
    assert False == less_than(data, 'c', 3)
    assert False == less_than(data, 'c', 4)
    assert True == less_than(data, 'c', 6)
    assert True == less_than(data, 'd', 10, extras=extras)
    assert True == less_than(data, 'd', 2, is_not=True, extras=extras)


def test_less_than_equal():
    data = {'a': 'b', 'c': 4, 'd': [1,2,3], 'e': {'h':1}}
    assert True == less_than_equal(data, 'c', 4)
    assert True == less_than_equal(data, 'd', 3, extras=extras)
    assert True == less_than_equal(data, 'd', 2, is_not=True, extras=extras)


def test_greater_than():
    data = {'a': 'b', 'c': 4, 'd': [1,2,3], 'e': {'h':1}}
    assert False == greater_than(data, 'c', 6)
    assert False == greater_than(data, 'c', 4)
    assert True == greater_than(data, 'c', 2)
    assert True == greater_than(data, 'd', 2, extras=extras)
    assert True == greater_than(data, 'd', 4, is_not=True, extras=extras)


def test_greater_than_equal():
    data = {'a': 'b', 'c': 4, 'd': [1,2,3], 'e': {'h':1}}
    assert True == greater_than_equal(data, 'c', 4)
    assert True == greater_than_equal(data, 'd', 3, extras=extras)
    assert True == greater_than_equal(data, 'd', 4, is_not=True, extras=extras)


def test_exists():
    data = {'a': 'b', 'c': 4, 'd': [1, 2, 3], 'e': {'h': 1}}
    assert True == exists(data, 'c', None)
    assert True == exists(data, 'f', None, is_not=True)