"""All comparison functions."""

from processor.helper.json.json_utils import check_field_exists, get_field_value

def apply_extras(value, extras):
    for extra in extras:
        if extra == 'len':
            value = len(value)
    return value


def equality(data, loperand, roperand, is_not=False, extras=None):
    """ Compare and return value """
    value = get_field_value(data, loperand)
    eql = False
    if value:
        if extras:
            value = apply_extras(value, extras)
        if value == roperand:
            eql = True
    if is_not:
        eql = not eql
    return eql


def less_than(data, loperand, roperand, is_not=False, extras=None):
    """ Compare and return value """
    value = get_field_value(data, loperand)
    lt = False
    if value and value < roperand:
        if extras:
            value = apply_extras(value, extras)
        if value < roperand:
            lt = True
    if is_not:
         lt = not lt
    return lt


def less_than_equal(data, loperand, roperand, is_not=False, extras=None):
    """ Compare and return value """
    value = get_field_value(data, loperand)
    lte = False
    if value:
        if extras:
            value = apply_extras(value, extras)
        if value <= roperand:
            lte = True
    if is_not:
        lte = not lte
    return lte


def greater_than(data, loperand, roperand, is_not=False, extras=None):
    """ Compare and return value """
    value = get_field_value(data, loperand)
    gt = False
    if value and value > roperand:
        if extras:
            value = apply_extras(value, extras)
        if value > roperand:
            gt = True
    if is_not:
        gt = not gt
    return gt


def greater_than_equal(data, loperand, roperand, is_not=False, extras=None):
    """ Compare and return value """
    value = get_field_value(data, loperand)
    gte = False
    if value and value >= roperand:
        if extras:
            value = apply_extras(value, extras)
        if value >= roperand:
            gte = True
    if is_not:
        gte = not gte
    return gte


def exists(data, loperand, roperand, is_not=False, extras=None):
    """ Compare and return value """
    present = check_field_exists(data, loperand)
    if is_not:
        present = not present
    return present


