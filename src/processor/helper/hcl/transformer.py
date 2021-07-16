
from typing import List
from hcl2.transformer import DictTransformer

class HClDictTransformer(DictTransformer):
    
    def full_splat(self, args: List) -> str:
        return ".".join(args)
    
    def full_splat_expr_term(self, args: List) -> str:
        return "%s[*].%s" % (args[0], args[1])
