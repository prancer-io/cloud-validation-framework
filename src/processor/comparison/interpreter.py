"""
Define an interface for creating an object, but let subclasses decide
which class to instantiate. Factory Method lets a class defer
instantiation to subclasses.
"""
import time
import sys
import json
import logging
import os
import re
import pymongo
import subprocess
from processor.helper.json.json_utils import get_field_value, json_from_file, save_json_to_file
from processor.helper.config.config_utils import get_test_json_dir, parsebool, config_value, generateid
from processor.helper.file.file_utils import exists_file, exists_dir, remove_file
from processor.database.database import COLLECTION, get_documents
from processor.comparison.comparison_functions import equality,\
    less_than, less_than_equal, greater_than, greater_than_equal, exists
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener, ConsoleErrorListener
from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter
from processor.helper.config.rundata_utils import get_dbtests, get_from_currentdata
from processor.logging.log_handler import getlogger
import traceback


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

class MyConsoleErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        logger.debug("******line " + str(line) + ":" + str(column) + " " + msg)

ConsoleErrorListener.INSTANCE = MyConsoleErrorListener()


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
    if not opa_exe:
        try:
            subprocess.Popen(['opa', "version"], stdout=subprocess.DEVNULL)
            opa_exe = "opa"
        except FileNotFoundError:
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


def import_from(module, name):
    try:
        module = __import__(module, fromlist=[name])
        return getattr(module, name)
    except:
        return

def import_module(module):
    try:
        module = __import__(module)
        return module
    except:
        logger.debug(traceback.format_exc())
        return False

class Comparator:
    """
    Declare the factory method, which returns a comparator object.
    Comparator also defines the default implementation of the factory
    method that returns a Concrete Comparator object based on the version.
    Call the factory method to create the comparator object.
    """

    def __init__(self, version, container, dbname, collection_data, testcase, excludedTestIds, includeTests):
        self.comparator = self._factory_method(version, container, dbname, collection_data,
                                               testcase, excludedTestIds, includeTests)

    @staticmethod
    def _factory_method(version, container, dbname, collection_data, testcase, excludedTestIds, includeTests):
        version_val = version_str(version)
        if version_val == COMPARATOR_V0_1:
            return ComparatorV01(container, dbname, collection_data, testcase, excludedTestIds, includeTests)
        elif version_val == COMPARATOR_V0_2:
            return ComparatorV02(container, dbname, collection_data, testcase, excludedTestIds, includeTests)
        else:
            return ComparatorV01(container, dbname, collection_data, testcase, excludedTestIds, includeTests)

    def validate(self):
        return self.comparator.validate()


class ComparatorV01:
    """Override the validate method to return to run comparator"""

    def __init__(self, container, dbname, collection_data, testcase, excludedTestIds, includeTests):
        self.container = container
        self.dbname = dbname
        self.collection_data = collection_data
        self.testcase = testcase
        self.excludedTestIds = excludedTestIds
        self.includeTests = includeTests
        loperand = get_field_value(testcase, 'attribute')
        value = get_field_value(testcase, 'comparison')
        rule = get_field_value(testcase, 'rule')
        isrego = get_field_value(testcase, 'type')
        self.snapshots = []
        if isrego and isrego == 'rego' or isrego == "python":
            self.format = TESTCASEV2
            self.rule = rule
            self.type = isrego
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

    def log_compliance_info(self, test_id, sid_pair=None):
        logger.critical('\tTESTID: %s', test_id)
        if sid_pair:
            logger.critical('\t\tSNAPSHOTID: %s', sid_pair)
        else:
            logger.critical('\t\tSNAPSHOTID: %s', self.testcase['snapshotId'][0])
        if self.snapshots:
            snapshot = self.snapshots[0]
            logger.critical('\t\tPATHS: ')
            for path in snapshot.get('paths', []):
                logger.critical('\t\t\t %s', path)

    def process_rego_test_case(self):
        tid = '%d_%s' % (int(time.time() * 1000000), generateid(None))
        results = []
        inputjson = {}
        result = False
        rule_expr = get_field_value(self.testcase, 'eval')
        if not rule_expr:
            rule_expr = get_field_value(self.testcase, 'evals')
            if rule_expr:
                del self.testcase['evals']
        if not rule_expr:
            rule_expr = 'data.rule.rulepass'
        testId = 'MISSING ID'
        isMasterTest = False
        if 'testId' in self.testcase:
            testId = self.testcase['testId']
        elif 'masterTestId' in self.testcase:
            testId = self.testcase['masterTestId']
            isMasterTest = True

                            
        # logger.critical('\t\tEVAL: %s', rule_expr)
        opa_exe = opa_binary()
        if not opa_exe:
            # print('*' * 50)
            logger.error('\t\tERROR: OPA binary not found!')
            logger.error('\t\tRESULT: FAILED')
            results.append({'eval': 'data.rule.rulepass', 'result': "passed" if result else "failed", 'message': ''})
            return results

        if len(self.testcase['snapshotId'])==1:
            sid = self.testcase['snapshotId'][0]
            toExclude, snapshot_doc = self.get_snaphotid_doc(sid, testId, isMasterTest)
            if toExclude:
                logger.warn('\t\tWARN: Excluded test case: %s' % testId)
                logger.warn('\t\tRESULT: SKIPPED')
                # msg = 'Excluded testcase because of testId: %s' % testId
                # results.append({'eval': 'data.rule.rulepass', 'result': 'skipped', 'message': msg})
                return results
            inputjson = snapshot_doc
            if inputjson is None:
                logger.info('\t\tERROR: Missing snapshot')
            results = []
            if inputjson:
                results = self.generating_result_for_rego_testcase(inputjson, tid, testId, opa_exe, rule_expr, results)
            else:
                results.append({'eval': rule_expr, 'result': "passed" if result else "failed", 'message': ''})
                self.log_result(results[-1])
            return results
        else:
            # ms_id = dict(zip(self.testcase['snapshotId'], self.testcase['masterSnapshotId']))
            # logger.info("ms_id")
            # logger.info(ms_id) 
            self.snapshots = []
            resource_sid = []
            for mastersnapshot_id in self.testcase['masterSnapshotId']:
                msid = []
                for sid in self.testcase['snapshotId']:
                    if sid.startswith(mastersnapshot_id):
                        msid.append(sid)
                resource_sid.append({mastersnapshot_id:msid})
            inputjson = {}
            for sid_pair in resource_sid:    
                for ms_id, s_id_list in sid_pair.items():
                    snapshot_doc_list = []
                    for s_id in s_id_list:
                        toExclude, snapshot_doc = self.get_snaphotid_doc(s_id, testId, isMasterTest)
                        if toExclude:
                            logger.warn('\t\tWARN: Excluded test case: %s' % testId)
                            logger.warn('\t\tRESULT: SKIPPED')
                            return results
                        snapshot_doc_list.append(snapshot_doc)
                    input = {ms_id: snapshot_doc_list}
                    inputjson.update(input)
            # print('inputjson: ', inputjson)
            if inputjson:
                results = self.generating_result_for_rego_testcase(inputjson, tid, testId, opa_exe, rule_expr, results, resource_sid)
            else:
                results.append({'eval': rule_expr, 'result': "passed" if result else "failed", 'message': ''})
                self.log_result(results[-1])
            return results

    def generating_result_for_rego_testcase(self, inputjson, tid, testId, opa_exe, rule_expr, results, sid_pair=None):
        save_json_to_file(inputjson, '/tmp/input_%s.json' % tid)
        rego_rule = self.rule
        rego_match=re.match(r'^file\((.*)\)$', rego_rule, re.I)
        if rego_match:
            rego_file = self.rego_rule_filename(rego_match.groups()[0], self.container)
            if rego_file:
                pass
            else:
                rego_file = None
        else:
            rego_txt = [
                "package rule",
                "default rulepass = false",
                "rulepass = true{",
                "   %s" % rego_rule,
                "}", ""
            ]
            rego_file = '/tmp/input_%s.rego' % tid
            open(rego_file, 'w').write('\n'.join(rego_txt))
        if rego_file:
            if isinstance(rule_expr, list):
                result = os.system('%s eval -i /tmp/input_%s.json -d %s "data.rule" > /tmp/a_%s.json' % (opa_exe, tid, rego_file, tid))
                if result != 0 :
                    self.log_compliance_info(testId)
                    logger.error("\t\tERROR: have problem in running opa binary")
                    self.log_rego_error(json_from_file("/tmp/a_%s.json" % tid, object_pairs_hook=None))
            else:
                result = os.system('%s eval -i /tmp/input_%s.json -d %s "%s" > /tmp/a_%s.json' % (opa_exe, tid, rego_file, rule_expr, tid))
                if result != 0 :
                    self.log_compliance_info(testId)
                    logger.error("\t\tERROR: have problem in running opa binary")
                    self.log_rego_error(json_from_file("/tmp/a_%s.json" % tid, object_pairs_hook=None))

            resultval = json_from_file('/tmp/a_%s.json' % tid)
            if resultval and "errors" in resultval and resultval["errors"]:
                if isinstance(rule_expr, list):
                    if rule_expr[0] and "eval" in rule_expr[0]:
                        results.append({'eval': rule_expr[0].get("eval"), 'result': "failed", 'message': ''})
                    else:
                        results.append({'eval': "data.rule", 'result': "failed", 'message': ''})
                else:
                    results.append({'eval': rule_expr, 'result': "failed", 'message': ''})
                self.log_compliance_info(testId)
                logger.critical('\t\tTITLE: %s', self.testcase.get('title', ""))
                logger.critical('\t\tDESCRIPTION: %s', self.testcase.get('description', ""))
                logger.critical('\t\tRULE: %s', self.testcase.get('rule', ""))
                logger.critical('\t\tERROR: %s', str(resultval["errors"]))
                logger.critical('\t\tREMEDIATION: %s', self.testcase.get('remediation_description', ""))
                logger.error('\t\tRESULT: FAILED')
                # logger.error(str(resultval["errors"]))
            elif resultval:
                if isinstance(rule_expr, list):
                    resultdict = resultval['result'][0]['expressions'][0]['value']
                    for val in rule_expr:
                        if 'eval' in val: 
                            evalfield = val['eval'].rsplit('.', 1)[-1]
                            evalmessage = val['message'].rsplit('.', 1)[-1] if "message" in val else ""
                            if evalfield in resultdict:
                                if isinstance(resultdict[evalfield], bool):
                                    result = parsebool(resultdict[evalfield])
                                else:
                                    if logger.level == logging.DEBUG:
                                        self.log_compliance_info(testId)
                                        logger.warning('\t\tRESULT: SKIPPED')
                                    continue
                            elif evalmessage in resultdict:
                                result = False
                            else:
                                if logger.level == logging.DEBUG:
                                    self.log_compliance_info(testId)
                                    logger.warning('\t\tRESULT: SKIPPED')
                                continue
                            msg = resultdict[evalmessage] if not result and evalmessage in resultdict else ""
                            results.append({
                                'eval': val["eval"], 
                                'result': "passed" if result else "failed", 
                                'message': msg,
                                'id' : val.get("id"),
                                'remediation_description' : val.get("remediationDescription"),
                                'remediation_function' : val.get("remediationFunction"),
                            })
                            # logger.info('\t\tERROR: %s', resultval)
                            self.log_compliance_info(testId, sid_pair)
                            self.log_result(results[-1])
                else:
                    resultbool = resultval['result'][0]['expressions'][0]['value'] # [get_field_value(resultval, 'result[0].expressions[0].value')
                    result = parsebool(resultbool)
                    results.append({'eval': rule_expr, 'result': "passed" if result else "failed", 'message': ''})
                    # logger.info('\t\tERROR: %s', resultval)
                    self.log_compliance_info(testId)
                    self.log_result(results[-1])
                    if results[-1]['result'] == 'failed':
                        logger.error('\t\tERROR: %s', json.dumps(dict(resultval)))

        else:
            if logger.level == logging.DEBUG:
                self.log_compliance_info(testId)
                logger.info('\t\tERROR: %s missing', rego_match.groups()[0])
                logger.warning('\t\tRESULT: SKIPPED')
            # results.append({'eval': rule_expr, 'result': "passed" if result else "failed", 'message': ''})
            # self.log_result(results[-1])
        remove_file('/tmp/input_%s.json' % tid)
        remove_file('/tmp/a_%s.json' % tid)
        return results

    def process_python_test_case(self) -> list:
        # setting path of tmp to allow import from temp
        sys.path.append('/tmp/')
        results = []
        inputjson = {}
        result = False

        # getting rule_expr value from evals or eval
        rule_expr = get_field_value(self.testcase, 'eval')
        if not rule_expr:
            rule_expr = get_field_value(self.testcase, 'evals')
            if rule_expr:
                del self.testcase['evals']
        if not rule_expr:
            rule_expr = 'data.rule.rulepass'

        # getting testId or MasterTestId
        testId = 'MISSING ID'
        isMasterTest = False
        if 'testId' in self.testcase:
            testId = self.testcase['testId']
        elif 'masterTestId' in self.testcase:
            testId = self.testcase['masterTestId']
            isMasterTest = True
        

        snapshot_id = self.testcase['snapshotId'][0]

        # getting snapshot and exclude status
        toExclude, snapshot_doc = self.get_snaphotid_doc(snapshot_id, testId, isMasterTest)
        if toExclude:
            logger.warn('\t\tWARN: Excluded test case: %s' % testId)
            logger.warn('\t\tRESULT: SKIPPED')
            return results
        
        # python file name
        python_testcase = self.rule.split(".")[0]
        # python function name

        if len(self.testcase['snapshotId']) == 1:
            inputjson = snapshot_doc
            if inputjson is None:
                logger.info('\t\tERROR: Missing snapshot')
        else:
            ms_id = dict(zip(self.testcase['snapshotId'], self.testcase['masterSnapshotId']))
            for sid in self.testcase['snapshotId']:
                toExclude, snapshot_doc = self.get_snaphotid_doc(sid, testId, isMasterTest)
                if toExclude:
                    logger.error('Excluded testcase because of testId: %s' % testId)
                inputjson.update({ms_id[sid]: snapshot_doc})
        results = []

        if inputjson:
            test_rule = self.rule
            rule_matched = re.match(r'^file\((.*)\)$', test_rule, re.I)
            if rule_matched:
                rego_file_name = self.rego_rule_filename(rule_matched.groups()[0], self.container)
                if not rego_file_name:
                    python_testcase = "processor.comparison.rules.%s.%s"%(self.snapshots[0]["type"],rule_matched.groups()[0].split(".")[0])
                    module = import_module(python_testcase)
                    if not module and logger.level == logging.DEBUG:
                        self.log_compliance_info(testId)
                        logger.error('\t\tERROR: %s missing', rule_matched.groups()[0])
                        logger.warning('\t\tRESULT: SKIPPED')
                        return results
                else:
                    python_testcase = rule_matched.groups()[0].split(".")[0]

            if isinstance(rule_expr, list):
                for rule in rule_expr:
                    function_name = rule["eval"].rsplit(".", 1)[-1] if "eval" in rule else ""
                    evalmessage = rule['message'].rsplit('.', 1)[-1] if "message" in rule else ""

                    test_function = import_from(python_testcase, function_name)
                    if not test_function:
                        self.log_compliance_info(testId)
                        logger.info('\t\tERROR: %s missing', rule_matched.groups()[0])
                        logger.warning('\t\tRESULT: SKIPPED')
                        return results
                
                    paths = self.snapshots[0]["paths"]

                    result = test_function(inputjson, kwargs={"paths": paths})

                    if result.get("issue") == True:
                        result["result"] = "failed"
                    
                        self.log_compliance_info(testId)
                        self.log_result(result)
                        json_result = {
                            'eval': rule["eval"], 
                            'result': result["result"], 
                            'message': result.get(evalmessage, ""),
                            'id' : rule.get("id"),
                            'remediation_description' : rule.get("remediationDescription"),
                            'remediation_function' : rule.get("remediationFunction"),
                        }

                        if result.get("errors"):
                            json_result["errors"] = result.get("errors",[])

                        results.append(json_result)

                    elif result.get("issue") == False:
                        if logger.level == logging.DEBUG:
                            self.log_compliance_info(testId)
                            logger.info('\t\tERROR: %s missing', rule_matched.groups()[0])
                            logger.warning('\t\tRESULT: SKIPPED')
                
                    elif result["issue"] == None:
                        logger.error("\t\tERROR: have problem in running test")
                        logger.error(result[evalmessage])

        return results
                

    def log_rego_error(self, result):
        """ 
        log error raised while running the rego file
        """
        if result and "errors" in result and result.get("errors"):
            error = result.get("errors")[0]
            location = error.get("location")
            logger.error('\t\t  %s' % error.get("message"))
            
            if location:
                file_location = "/".join(location.get("file", "").split("/")[3:])
                logger.error("\t\t  location : %s" % file_location)
                logger.error("\t\t  row : %s" % location.get("row"))
                logger.error("\t\t  col : %s" % location.get("col"))
                
    def log_result(self, result):
        if result.get("result") == "passed":
            logger.critical('\t\tTITLE: %s', self.testcase.get('title', ""))
            logger.critical('\t\tRULE: %s', self.testcase.get('rule', ""))
            logger.critical('\t\tRESULT: %s', result.get("result"), extra={"type" : "SUCCESS"})            
        else:
            logger.critical('\t\tTITLE: %s', self.testcase.get('title', ""))
            logger.critical('\t\tDESCRIPTION: %s', self.testcase.get('description', ""))
            logger.critical('\t\tRULE: %s', self.testcase.get('rule', ""))
            logger.critical('\t\tERROR: %s', result.get("message", ""))
            logger.critical('\t\tREMEDIATION: %s', result.get('remediation_description', ""))
            logger.error('\t\tRESULT: %s', result.get("result"))

    def get_snaphotid_doc_old(self, sid, container):
        doc = None
        json_dir = get_test_json_dir()
        if exists_dir(json_dir):
            fname = '%s/%s/snapshots/%s' % (json_dir, container, sid)
            if exists_file(fname):
                json_data = json_from_file(fname)
                if json_data and 'json' in json_data:
                    doc = json_data['json']
                    snapshot = {
                        'id': json_data['snapshotId'],
                        'structure': json_data['structure'],
                        'reference': json_data['reference'],
                        'source': json_data['source'],
                        'collection': json_data['collection'],
                        'type': json_data.get("node", {}).get('type'),
                        'region' : json_data.get('region', "")
                    }
                    if 'paths' in json_data:
                        snapshot['paths'] = json_data['paths']
                    else:
                        snapshot['path'] = json_data['path']

                    self.snapshots.append(snapshot)
        return doc

    def exclude_test_case(self, doc, testId, isMasterTest=False):
        toExclude = False
        if isMasterTest and testId:
            if testId in self.includeTests:
                toExclude = False
            elif testId in self.excludedTestIds:
                path = doc['paths'][0]
                toExclude = True if path in self.excludedTestIds[testId] else False
            else:
                if 'evals' in self.testcase and self.testcase['evals']:
                    found = False
                    for eval in self.testcase['evals']:
                        if eval['id'] in self.includeTests:
                            found = True
                            break
                    if not found:
                        for eval in self.testcase['evals']:
                            if eval['id'] in self.excludedTestIds:
                                path = doc['paths'][0]
                                toExclude = True if path in self.excludedTestIds[eval['id']] else False
        return toExclude

    def get_snaphotid_doc(self, sid, testId, isMasterTest=False):
        tobeExcluded = False
        doc = None
        isdb_fetch = get_dbtests()
        if isdb_fetch:
            dbname = self.dbname
            coll = self.collection_data[sid] if sid in self.collection_data else COLLECTION
            docs = get_documents(coll, {'snapshotId': sid}, dbname,
                                 sort=[('timestamp', pymongo.DESCENDING)], limit=1)
            logger.debug('Number of Snapshot Documents: %s', len(docs))
            if docs and len(docs):
                tobeExcluded = self.exclude_test_case(docs[0], testId, isMasterTest)
                doc = docs[0]['json']
                snapshot = {
                    'id': docs[0]['snapshotId'],
                    'structure': docs[0]['structure'],
                    'reference': docs[0]['reference'],
                    'source': docs[0]['source'],
                    'collection': docs[0]['collection'],
                    'type': docs[0].get("node", {}).get('type'),
                    'region' : docs[0].get('region', ""),
                    'resourceTypes' : docs[0].get("node", {}).get('resourceTypes', []),
                }
                if 'paths' in docs[0]:
                    snapshot['paths'] = docs[0]['paths']
                else:
                    snapshot['path'] = docs[0]['path']
                self.snapshots.append(snapshot)
        else:
            json_dir = '%s%s' % (get_test_json_dir(), self.container)
            if exists_dir(json_dir):
                fname = '%s/snapshots/%s' % (json_dir, sid)
                if exists_file(fname):
                    json_data = json_from_file(fname)
                    if json_data and 'json' in json_data:
                        tobeExcluded = self.exclude_test_case(json_data, testId, isMasterTest)
                        doc = json_data['json']
                        snapshot_val = {
                            'id': json_data['snapshotId'],
                            'structure': json_data['structure'],
                            'reference': json_data['reference'],
                            'source': json_data['source'],
                            'collection': json_data['collection'],
                            'type': json_data.get("node", {}).get('type'),
                            'region' : json_data.get('region', ""),
                            'resourceTypes' : json_data.get("node", {}).get('resourceTypes', []),
                        }
                        if 'paths' in json_data:
                            snapshot_val['paths'] = json_data['paths']
                        else:
                            snapshot_val['path'] = json_data['path']

                        # singletest = get_from_currentdata(SINGLETEST)
                        # if singletest:
                        #     snapshot_val['json'] = doc
                        self.snapshots.append(snapshot_val)
        return tobeExcluded, doc


    def rego_rule_filename(self, rego_file, container):
        rego_file_name = None
        if 'dirpath' in self.testcase and self.testcase['dirpath']:
            rego_file_name = '%s/%s' % (self.testcase['dirpath'], rego_file)
            if exists_file(rego_file_name):
                pass
            else:
                rego_file_name = None
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

    def get_connector_data(self):
        """ get connector data from snapshot """
        connector_data = {}
        if self.snapshots:
            isdb_fetch = get_dbtests()
            if isdb_fetch:
                connectors = get_documents(
                    "structures",
                    query={
                        "name" : self.snapshots[0].get("source"),
                        "type" : "structure",
                        "container": self.container
                    },
                    dbname=self.dbname,
                    limit=1
                )
                connector_data = connectors[0].get("json", {}) if connectors else {}
            else:
                json_test_dir = get_test_json_dir()
                snapshot_source = self.snapshots[0].get("source")
                file_name = '%s.json' % snapshot_source if snapshot_source and not \
                    snapshot_source.endswith('.json') else snapshot_source
                connector_path = '%s/../%s' % (json_test_dir, file_name)
                if exists_file(connector_path):
                    connector_data = json_from_file(connector_path)

        return connector_data

    def validate(self):
        result_val = [{"result": "failed"}]
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
                        result_val[0]["result"] = "passed" if result else "failed"
                        result_val[0]["snapshots"] = [{
                            'id': docs[0]['snapshotId'],
                            'structure': docs[0]['structure'],
                            'reference': docs[0]['reference'],
                            'source': docs[0]['source'],
                            'collection': docs[0]['collection']
                        }]
                        if "paths" in docs[0]:
                            result_val[0]["snapshots"][0]["paths"] = docs[0]["paths"]
                        else:
                            result_val[0]["snapshots"][0]["path"] = docs[0]["path"]
                else:
                    result_val[0].update({
                        "result": "skipped",
                        "message": "Missing documents for the snapshot"
                    })
            else:
                result_val[0].update({
                    "result": "skipped",
                    "message": "Missing snapshotId for testcase"
                })
        elif self.format == TESTCASEV2:
            if self.type == 'rego':
                results = self.process_rego_test_case()
                result_val = []
                connector_data = self.get_connector_data()
                for result in results:
                    result['snapshots'] = self.snapshots
                    result['autoRemediate'] = connector_data.get("autoRemediate", False)
                    result_val.append(result)
            
            elif self.type == "python":
                results = self.process_python_test_case()
                result_val = []
                connector_data = self.get_connector_data()
                for result in results:
                    result['snapshots'] = self.snapshots
                    result['autoRemediate'] = connector_data.get("autoRemediate", False)
                    result_val.append(result)
            
            else:
                # logger.info('#' * 75)
                logger.critical('\tTESTID: %s', self.testcase['testId'])
                input_stream = InputStream(self.rule)
                lexer = comparatorLexer(input_stream)
                stream = CommonTokenStream(lexer)
                parser = comparatorParser(stream)
                tree = parser.expression()
                children = []
                for child in tree.getChildren():
                    children.append((child.getText()))
                # logger.info('*' * 50)
                logger.debug("All the parsed tokens: %s", children)
                otherdata = {'dbname': self.dbname, 'snapshots': self.collection_data, 'container': self.container}
                r_i = RuleInterpreter(children, **otherdata)
                # result = r_i.compare()
                l_val, r_val, result = r_i.compare()
                result_val[0]["result"] = "passed" if result else "failed"
                result_val[0]['snapshots'] = r_i.get_snapshots()
                connector_data = self.get_connector_data()
                result_val[0]['autoRemediate'] = connector_data.get("autoRemediate", False)
                if result_val[0]['snapshots']:
                    snapshot = result_val[0]['snapshots'][0]
                    logger.critical('\t\tSNAPSHOTID: %s', snapshot['id'])
                    logger.critical('\t\tPATHS: ')
                    for path in snapshot.get('paths', []):
                        logger.critical('\t\t\t %s', path)
                if not result:
                    logger.critical('\t\tLHS: %s', l_val)
                    logger.critical('\t\tRHS: %s', r_val)
                self.log_result(result_val[0])
        else:
            result_val[0].update({
                "result": "skipped",
                "reason": "Unsupported testcase format"
            })
        
        if 'dirpath' in self.testcase:
            del self.testcase['dirpath']
        return result_val


class ComparatorV02(ComparatorV01):
    """
    Override the validate method to run the comparisons
    """
    def __init__(self, container, dbname, collection_data, testcase, excludedTestIds, includeTests):
        ComparatorV01.__init__(self, container, dbname, collection_data, testcase, excludedTestIds, includeTests)

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
