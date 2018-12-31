""" Tests for validation"""


def test_comparatorLexer():
    from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
    val = comparatorLexer()
    assert val is not None

def test_comparatorListener():
    from antlr4 import InputStream, ParseTreeWalker
    from antlr4 import CommonTokenStream
    from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
    from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
    from processor.comparison.comparisonantlr.comparatorListener import comparatorListener
    input_stream = InputStream('exist({1}.location)')
    lexer = comparatorLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = comparatorParser(stream)
    tree = parser.expression()
    printer = comparatorListener()
    walker = ParseTreeWalker()
    print(walker.walk(printer, tree))

