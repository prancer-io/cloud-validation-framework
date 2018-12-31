# Generated from comparator.g4 by ANTLR 4.7.1
from antlr4 import ParseTreeListener
from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
from processor.logging.log_handler import getlogger

logger = getlogger()

# This class defines a complete listener for a parse tree produced by comparatorParser.
class comparatorListener(ParseTreeListener):

    # Enter a parse tree produced by comparatorParser#expression.
    def enterExpression(self, ctx:comparatorParser.ExpressionContext):
        logger.info("Enter context: %s", ctx.getText())

    # Exit a parse tree produced by comparatorParser#expression.
    def exitExpression(self, ctx:comparatorParser.ExpressionContext):
        logger.info("Exit context: %s", ctx.getText())