import json
from hcl.parser import HclParser, pickle_file
from hcl.api import u, isHcl
from hcl2.lark_parser import Lark_StandAlone
from processor.helper.hcl import yacc
from processor.helper.hcl.transformer import HClDictTransformer

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
    hcl2 = Lark_StandAlone(transformer=HClDictTransformer())
    return hcl2.parse(s + "\n")
    # s = u(s)
    # if isHcl(s):
    #     return TerraformHCLParer().parse(s)
    # else:
    #     return json.loads(s)