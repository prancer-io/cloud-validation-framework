"""
Define an interface for creating an object, but let subclasses decide
which class to instantiate. Factory Method lets a class defer
instantiation to subclasses.
"""
import re
from processor.helper.comparison.comparison_functions import equality,\
    less_than, less_than_equal,greater_than, greater_than_equal, exists
from processor.logging.log_handler import getlogger


logger = getlogger()
COMPARATOR_V0_1 = '0_1'
COMPARATOR_V0_2 = '0_2'
OPERATORS = {
    'eq': equality,
    'neq': equality,
    'lt': less_than,
    'le': less_than_equal,
    'gt': greater_than,
    'ge': greater_than_equal,
    'not': None,
    'exist': exists
}
MATHOPERATORS = ['lt', 'le', 'gt', 'ge', 'eq', 'neq']


def version_str(version):
    """Convert numeric version to string eg: 0.1 => 0_1"""
    value = version.replace('.', '_') if version else version
    return value


def get_operator_roperand(value):
    roperand = None,
    op = 'exist'
    is_not = False
    extras = None
    if value:
        if value.startswith('not') or value.startswith('neq'):
            is_not = True
            value = value.replace('not', '') if value.startswith('not') \
                else value.replace('neq', 'eq')
            value = value.strip()
        vals = value.split()
        if vals and vals[0] in OPERATORS:
            op = vals[0]
            if len(vals) > 1:
                roperand = ' '.join(vals[1:])
        else:
            roperand = value
        if roperand:
            is_math = True if op in MATHOPERATORS else False
            extras, roperand = adapt_roperand(roperand, is_math)
    return is_not, op, roperand, extras


def adapt_roperand(roperand, is_math=False):
    value = roperand
    extras = None
    if is_math:
        try:
            value = int(roperand)
        except:
            pass
    if value and not isinstance(value, int):
        if value[0] == '"' and value[-1] == '"':
            value = value.replace('"', '')
        elif value[0] == "'" and value[-1] == "'":
            value = value.replace("'", "")
        extended_value = interpret_additional_operations(value)
        if extended_value:
            value = list(extended_value.values()).pop(0)
            extras = list(extended_value.keys())
    return extras, value


def match_array_len(_, roperand):
    value = int(roperand[4:-1])
    return {'len': value}


def fetch_snapshot_attribute(m, roperand):
    pass


def interpret_additional_operations(roperand):
    value = None
    actions = ((r'len\(\d+\)', match_array_len),
               (r'\{2\}\.(.*)', fetch_snapshot_attribute))
    try:
        for regex, action in actions:
            m = re.match(regex, roperand, re.I)
            if m:
                # print(m.groups(), regex)
                value = action(m, roperand)
                break
    except:
        pass
    return value


class Comparator:
    """
    Declare the factory method, which returns a comparator object.
    Comparator also defines the default implementation of the factory
    method that returns a Concrete Comparator object based on the version.
    Call the factory method to create the comparator object.
    """

    def __init__(self, version, data, loperand, value):
        self.comparator = self._factory_method(version, data, loperand, value)

    def _factory_method(self, version, data, loperand, value):
        version_val = version_str(version)
        if version_val == COMPARATOR_V0_1:
            return Comparator_v0_1(data, loperand, value)
        elif version_val == COMPARATOR_V0_2:
            return Comparator_v0_2(data, loperand, value)
        else:
            return Comparator_v0_1(data, loperand, value)

    def validate(self):
        try:
            return self.comparator.validate()
        except:
            return False


class Comparator_v0_1:
    """
    Override the validate method to return to run comparator
    """

    def __init__(self, data, loperand, value):
        self.data = data
        self.loperand = loperand
        self.is_not, self.op, self.roperand, self.extras = get_operator_roperand(value)

    def validate(self):
        if self.op in OPERATORS and OPERATORS[self.op]:
            return OPERATORS[self.op](self.data, self.loperand, self.roperand, self.is_not,
                                      self.extras)
        return False


class Comparator_v0_2(Comparator_v0_1):
    """
    Override the validate method to run the comparisons
    """
    def __init__(self, data, loperand, value):
        super(data, loperand, value)

    def validate(self):
        return super(Comparator_v0_1, self).validate()


def main():
    comparator = Comparator('0.1', {'a': 'b'}, 'a', 'exist')
    print(type(comparator))
    print(type(comparator.comparator))
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b'}, 'b', 'exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b'}, 'b', 'not exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c':{'d': 1}}, 'c.e', 'not exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 1}}, 'c.d', 'not exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 1}}, 'c.d', 'exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'gt 10')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'eq 10')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'neq 5')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'eq "eastus"')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'eq len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'neq len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'gt len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'gte len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'lt len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'lte len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', "eq '{2}.location'")
    print(comparator.validate())

if __name__ == "__main__":
    main()
