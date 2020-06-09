"""
Define an interface for creating an object, but let subclasses decide
which class to instantiate. Factory Method lets a class defer
instantiation to subclasses.
"""
import os
import re
import pymongo
from processor.helper.json.json_utils import get_field_value, json_from_file, save_json_to_file
from processor.helper.config.config_utils import get_test_json_dir, parsebool, config_value, SINGLETEST
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.database.database import COLLECTION, get_documents
from processor.comparison.comparison_functions import equality,\
    less_than, less_than_equal, greater_than, greater_than_equal, exists
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter
from processor.helper.config.rundata_utils import get_dbtests, get_from_currentdata
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


def opa_binary():
    opa_exe = None
    opa_enabled = parsebool(config_value("OPA", "opa"), False)
    if opa_enabled:
        opa_exe = os.getenv('OPAEXE', None)
        # print(opa_exe)
        if opa_exe and exists_file(opa_exe):
            # print('%' * 50)
            pass
        else:
            # print('$' * 50)
            opa_exe = config_value("OPA", "opaexe")
            if opa_exe and exists_file(opa_exe):
                pass
            else:
                opa_exe = None
    return opa_exe


def get_rego_rule_filename(rego_file, container):
    rego_file_name = None
    json_dir = get_test_json_dir()
    if exists_dir(json_dir):
        rego_file_name = '%s/%s/%s' % (json_dir, container, rego_file)
        if exists_file(rego_file_name):
            pass
        else:
            rego_file_name = None
    return rego_file_name


def compare(inputjson, rulestr):
   pass


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
        self.testcase = testcase
        loperand = get_field_value(testcase, 'attribute')
        value = get_field_value(testcase, 'comparison')
        rule = get_field_value(testcase, 'rule')
        isrego = get_field_value(testcase, 'type')
        self.snapshots = []
        if isrego and isrego == 'rego':
            self.format = TESTCASEV2
            self.rule = rule
            self.type = 'rego'
        elif loperand and value:
            self.format = TESTCASEV1
            self.snapshot_id = get_field_value(testcase, 'snapshotId')
            coll_val = get_field_value(self.collection_data, self.snapshot_id)
            self.collection = coll_val if coll_val else COLLECTION
            self.loperand = loperand
            self.is_not, self.op, self.roperand, self.extras = get_operator_roperand(value)
            self.type = 'prancer'
        elif rule:
            self.format = TESTCASEV2
            self.rule = rule
            self.type = 'prancer'
        else:
            self.format = None

    def process_rego_test_case(self):
        inputjson = {}
        result = False
        opa_exe = opa_binary()
        if not opa_exe:
            # print('*' * 50)
            return result
        rule_expr = get_field_value(self.testcase, 'eval')
        if not rule_expr:
            rule_expr = 'data.rule.rulepass'
        if len(self.testcase['snapshotId'])==1:
            sid = self.testcase['snapshotId'][0]
            inputjson = self.get_snaphotid_doc(sid)
        else:
            ms_id = dict(zip(self.testcase['snapshotId'], self.testcase['masterSnapshotId']))
            for sid in self.testcase['snapshotId']:
                inputjson.update({ms_id[sid]: self.get_snaphotid_doc(sid)})
        if inputjson:
            save_json_to_file(inputjson, '/tmp/input.json')
            rego_rule = self.rule
            rego_match=re.match(r'^file\((.*)\)$', rego_rule, re.I)
            if rego_match:
                # rego_file = get_rego_rule_filename(rego_match.groups()[0], self.container)
                rego_file = self.rego_rule_filename(rego_match.groups()[0], self.container)
                if rego_file:
                    pass
                else:
                    rego_file = None
                # rego_file1 = self.rego_rule_filename(rego_match.groups()[0], "google_crawler_container")
                # rego_file1 = self.rego_rule_filename('google_crawler.rego', "google_crawler_container")
                # print(rego_file1)
            else:
                rego_txt = [
                    "package rule",
                    "default rulepass = false",
                    "rulepass = true{",
                    "   %s" % rego_rule,
                    "}", ""
                ]
                rego_file = '/tmp/input.rego'
                open(rego_file, 'w').write('\n'.join(rego_txt))
            if rego_file:
                os.system('%s eval -i /tmp/input.json -d %s "%s" > /tmp/a.json' % (opa_exe, rego_file, rule_expr))
                resultval = json_from_file('/tmp/a.json')
                if resultval:
                    resultbool = resultval['result'][0]['expressions'][0]['value'] # [get_field_value(resultval, 'result[0].expressions[0].value')
                    if resultbool:
                        result = parsebool(resultbool)
            else:
                result = False
        return result



    def get_snaphotid_doc_old(self, sid, container):
        doc = None
        json_dir = get_test_json_dir()
        if exists_dir(json_dir):
            fname = '%s/%s/snapshots/%s' % (json_dir, container, sid)
            if exists_file(fname):
                json_data = json_from_file(fname)
                if json_data and 'json' in json_data:
                    doc = json_data['json']
                    self.snapshots.append({
                        'id': json_data['snapshotId'],
                        'path': json_data['path'],
                        'structure': json_data['structure'],
                        'reference': json_data['reference'],
                        'source': json_data['source']
                    })
        return doc


    def get_snaphotid_doc(self, sid):
        doc = None
        isdb_fetch = get_dbtests()
        if isdb_fetch:
            dbname = self.dbname
            coll = self.collection_data[sid] if sid in self.collection_data else COLLECTION
            docs = get_documents(coll, {'snapshotId': sid}, dbname,
                                 sort=[('timestamp', pymongo.DESCENDING)], limit=1)
            logger.debug('Number of Snapshot Documents: %s', len(docs))
            if docs and len(docs):
                doc = docs[0]['json']
                self.snapshots.append({
                    'id': docs[0]['snapshotId'],
                    'path': docs[0]['path'],
                    'structure': docs[0]['structure'],
                    'reference': docs[0]['reference'],
                    'source': docs[0]['source']
                })
        else:
            json_dir = '%s%s' % (get_test_json_dir(), self.container)
            if exists_dir(json_dir):
                fname = '%s/snapshots/%s' % (json_dir, sid)
                if exists_file(fname):
                    json_data = json_from_file(fname)
                    if json_data and 'json' in json_data:
                        doc = json_data['json']
                        snapshot_val = {
                            'id': json_data['snapshotId'],
                            'path': json_data['path'],
                            'structure': json_data['structure'],
                            'reference': json_data['reference'],
                            'source': json_data['source']
                        }
                        singletest = get_from_currentdata(SINGLETEST)
                        if singletest:
                            snapshot_val['json'] = doc
                        self.snapshots.append(snapshot_val)
        return doc


    def rego_rule_filename(self, rego_file, container):
        rego_file_name = None
        if 'dirpath' in self.testcase and self.testcase['dirpath']:
            rego_file_name = '%s/%s' % (self.testcase['dirpath'], rego_file)
            return  rego_file_name
        isdb_fetch = get_dbtests()
        #It give same value for DB and SNAPSHOT, So for SNAPSHOT, we'll check it in 
        #db first and if file isn't there, then we are fetching it from file path '''
        
        if isdb_fetch:
            dbname = self.dbname
            coll = 'structures'
            docs = get_documents(coll, { 'type': 'others', "container" : container}, dbname,
                                 sort=[('timestamp', pymongo.DESCENDING)], limit=1)
            # print('Number of other Documents: %s' % len(docs))
            logger.debug('Number of other Documents: %s', len(docs))
            if docs and len(docs):
                doc = docs[0]['json']
                if doc and 'file' in doc and isinstance(doc['file'], list):
                    for file_doc in doc['file']:
                        name = get_field_value(file_doc, 'name')
                        # print(name, rego_file)
                        if name == rego_file:
                            content = get_field_value(file_doc, 'container_file')
                            if content:
                                rego_file_name = '/tmp/%s' % rego_file
                                open(rego_file_name, 'w', encoding="utf-8").write(content)
                                return rego_file_name
                # print(doc)

        json_dir = get_test_json_dir()
        if exists_dir(json_dir):
            rego_file_name = '%s/%s/%s' % (json_dir, container, rego_file)
            if exists_file(rego_file_name):
                pass
            else:
                rego_file_name = None
        return rego_file_name


    def validate(self):
        result_val = {"result": "failed"}
        if self.format == TESTCASEV1:
            if self.snapshot_id:
                docs = get_documents(self.collection, dbname=self.dbname,
                                     sort=[('timestamp', pymongo.DESCENDING)],
                                     query={'snapshotId': self.snapshot_id},
                                     limit=1)
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
            if self.type == 'rego':
                result = self.process_rego_test_case()
                result_val["result"] = "passed" if result else "failed"
                result_val['snapshots'] = self.snapshots
            else:
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


def main(container):
    from processor.connector.validation import run_container_validation_tests_filesystem
    try:
        run_container_validation_tests_filesystem(container)
        return True
    except Exception as ex:
        print("Exception: %s" % ex)
        return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:        
        comparator = Comparator('0.1', 'validator', {}, {"testId": "4", "snapshotId1": "1", "attribute": "id", "comparison": "gt0 10"})
        val = comparator.validate()
        print(val)
