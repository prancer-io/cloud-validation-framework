"""
Define an interface for creating an object, but let subclasses decide
which class to instantiate. Factory Method lets a class defer
instantiation to subclasses.
"""
import re
import pymongo
from processor.helper.json.json_utils import get_field_value
from processor.database.database import COLLECTION, get_documents
from processor.comparison.comparison_functions import equality,\
    less_than, less_than_equal, greater_than, greater_than_equal, exists
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter

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
TESTCASEV1 = 1
TESTCASEV2 = 2


def version_str(version):
    """Convert numeric version to string eg: 0.1 => 0_1"""
    value = version.replace('.', '_') if version else version
    return value


def get_operator_roperand(value):
    roperand = None
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
    # try:
    for regex, action in actions:
        m = re.match(regex, roperand, re.I)
        if m:
            logger.debug(m.groups(), regex)
            value = action(m, roperand)
            break
    # except:
    #     pass
    return value


class Comparator:
    """
    Declare the factory method, which returns a comparator object.
    Comparator also defines the default implementation of the factory
    method that returns a Concrete Comparator object based on the version.
    Call the factory method to create the comparator object.
    """

    def __init__(self, version, container, dbname, collection_data, testcase):
        self.comparator = self._factory_method(version, container, dbname, collection_data, testcase)

    @staticmethod
    def _factory_method(version, container, dbname, collection_data, testcase):
        version_val = version_str(version)
        if version_val == COMPARATOR_V0_1:
            return ComparatorV01(container, dbname, collection_data, testcase)
        elif version_val == COMPARATOR_V0_2:
            return ComparatorV02(container, dbname, collection_data, testcase)
        else:
            return ComparatorV01(container, dbname, collection_data, testcase)

    def validate(self):
        return self.comparator.validate()


class ComparatorV01:
    """Override the validate method to return to run comparator"""

    def __init__(self, container, dbname, collection_data, testcase):
        self.container = container
        self.dbname = dbname
        self.collection_data = collection_data
        loperand = get_field_value(testcase, 'attribute')
        value = get_field_value(testcase, 'comparison')
        rule = get_field_value(testcase, 'rule')
        if loperand and value:
            self.format = TESTCASEV1
            self.snapshot_id = get_field_value(testcase, 'snapshotId')
            coll_val = get_field_value(self.collection_data, self.snapshot_id)
            self.collection = coll_val if coll_val else COLLECTION
            self.loperand = loperand
            self.is_not, self.op, self.roperand, self.extras = get_operator_roperand(value)
        elif rule:
            self.format = TESTCASEV2
            self.rule = rule
        else:
            self.format = None

    def validate(self):
        result_val = {"result": "failed"}
        if self.format == TESTCASEV1:
            if self.snapshot_id:
                docs = get_documents(self.collection, dbname=self.dbname,
                                     sort=[('timestamp', pymongo.DESCENDING)],
                                     query={'snapshotId': self.snapshot_id},
                                     limit=1)
                # docs = [{
                # "_id": "5c24af787456217c485ad1e6",
                # "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
                # "collection": "microsoftcompute",
                # "json":{
                #     "id": 124,
                #     "location": "eastus2",
                #     "name": "mno-nonprod-shared-cet-eastus2-tab-as03"
                # },
                # "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
                # "snapshotId": 1,
                # "timestamp": 1545908086831
                # }]
                logger.info('Number of Snapshot Documents: %s', len(docs))
                if docs and len(docs):
                    self.data = docs[0]['json']
                    if self.op in OPERATORS and OPERATORS[self.op]:
                        result = OPERATORS[self.op](self.data, self.loperand, self.roperand,
                                                    self.is_not, self.extras)
                        result_val["result"] = "passed" if result else "failed"
                        result_val["snapshots"] = [{
                            'id': docs[0]['snapshotId'],
                            'path': docs[0]['path'],
                            'structure': docs[0]['structure'],
                            'reference': docs[0]['reference'],
                            'source': docs[0]['source']
                        }]
                    # else:
                    #     result_val['reason'] = 'Unsupported comparison operator: %s' % self.op
                else:
                    result_val.update({
                        "result": "skipped",
                        "reason": "Missing documents for the snapshot"
                    })
            else:
                result_val.update({
                    "result": "skipped",
                    "reason": "Missing snapshotId for testcase"
                })
        elif self.format == TESTCASEV2:
            logger.info('#' * 75)
            logger.info('Actual Rule: %s', self.rule)
            input_stream = InputStream(self.rule)
            lexer = comparatorLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = comparatorParser(stream)
            tree = parser.expression()
            children = []
            for child in tree.getChildren():
                children.append((child.getText()))
            logger.info('*' * 50)
            logger.debug("All the parsed tokens: %s", children)
            otherdata = {'dbname': self.dbname, 'snapshots': self.collection_data, 'container': self.container}
            r_i = RuleInterpreter(children, **otherdata)
            result = r_i.compare()
            result_val["result"] = "passed" if result else "failed"
            result_val['snapshots'] = r_i.get_snapshots()
        else:
            result_val.update({
                "result": "skipped",
                "reason": "Unsupported testcase format"
            })
        return result_val


class ComparatorV02(ComparatorV01):
    """
    Override the validate method to run the comparisons
    """
    def __init__(self, container, dbname, collection_data, testcase):
        ComparatorV01.__init__(self, container, dbname, collection_data, testcase)

    def validate(self):
        return ComparatorV01.validate(self)


# if __name__ == "__main__":
#     comparator = Comparator('0.1', 'validator', {}, {
#         "testId": "4",
#         "snapshotId1": "1",
#         "attribute": "id",
#         "comparison": "gt0 10"
#     })
#     val = comparator.validate()
#     print(val)