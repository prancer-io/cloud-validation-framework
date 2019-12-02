"""All comparison functions."""

import math

EQ = '='
NEQ = '!='
GT = '>'
GTE = '>='
LT = '<'
LTE = '<='


int_funcs = {
    EQ: lambda lhs, rhs: lhs == rhs,
    NEQ: lambda lhs, rhs: lhs != rhs,
    GT: lambda lhs, rhs: lhs > rhs,
    GTE: lambda lhs, rhs: lhs >= rhs,
    LT: lambda lhs, rhs: lhs < rhs,
    LTE: lambda lhs, rhs: lhs <= rhs
}

float_funcs = {
    EQ: lambda lhs, rhs: math.isclose(lhs, rhs),
    NEQ: lambda lhs, rhs: not math.isclose(lhs, rhs),
    GT: lambda lhs, rhs: lhs > rhs,
    GTE: lambda lhs, rhs: lhs > rhs or math.isclose(lhs, rhs),
    LT: lambda lhs, rhs: lhs < rhs,
    LTE: lambda lhs, rhs: lhs < rhs or math.isclose(lhs, rhs)
}


def compare_none(loperand, roperand, op):
    if loperand is None and roperand is None:
        return True if op == EQ else False
    return False


def compare_int(loperand, roperand, op):
    if type(loperand) is int and type(roperand) is int:
        if op in int_funcs:
            return int_funcs[op](loperand, roperand)
    return False


def compare_float(loperand, roperand, op):
    if type(loperand) is float and type(roperand) is float:
        if op in float_funcs:
            return float_funcs[op](loperand, roperand)
    return False


def compare_boolean(loperand, roperand, op):
    if type(loperand) is bool and type(roperand) is bool:
        if op == EQ:
            return True if loperand == roperand else False
        elif op == NEQ:
            return True if loperand != roperand else False
    return False


def compare_str(loperand, roperand, op):
    if type(loperand) is str and type(roperand) is str:
        if op in int_funcs:
            return int_funcs[op](loperand, roperand)
    return False


def compare_list(loperand, roperand, op):
    if type(loperand) is list and type(roperand) is list:
        if op in int_funcs:
            return int_funcs[op](loperand, roperand)
    return False

def compare_in(loperand, roperand, op):
    if loperand and roperand:
        return roperand in loperand
    return False

def compare_dict(loperand, roperand, op):
    if type(loperand) is dict and type(roperand) is dict:
        if op in int_funcs:
            return int_funcs[op](loperand, roperand)
    return False
