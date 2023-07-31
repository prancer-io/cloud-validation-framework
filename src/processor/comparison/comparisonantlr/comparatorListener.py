# Generated from comparator.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .comparatorParser import comparatorParser
else:
    from comparatorParser import comparatorParser

# This class defines a complete listener for a parse tree produced by comparatorParser.
class comparatorListener(ParseTreeListener):

    # Enter a parse tree produced by comparatorParser#expression.
    def enterExpression(self, ctx:comparatorParser.ExpressionContext):
        pass

    # Exit a parse tree produced by comparatorParser#expression.
    def exitExpression(self, ctx:comparatorParser.ExpressionContext):
        pass



del comparatorParser