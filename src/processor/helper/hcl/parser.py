import json
from hcl.parser import HclParser, pickle_file
from hcl.api import u, isHcl
from processor.helper.hcl import yacc

class TerraformHCLParer(HclParser):
    def __init__(self):
        self.yacc = yacc.yacc(module=self, debug=False, optimize=1, picklefile=pickle_file)
    
    def parse(self, s):
        return self.yacc.parse(s, lexer=yacc.TerraformLexer())

def loads(fp):
    '''
    Deserializes a string and converts it to a dictionary. The contents
    of the string must either be JSON or HCL.
    
    :returns: Dictionary 
    '''
    s = fp.read()
    s = u(s)
    if isHcl(s):
        return TerraformHCLParer().parse(s)
    else:
        return json.loads(s)