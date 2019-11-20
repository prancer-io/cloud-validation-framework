import sys
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
from processor.comparison.comparisonantlr.rule_interpreter import RuleInterpreter


def main(argv):
    # input = FileStream(argv[1])
    try:
        with open(argv[1]) as f:
            for line in f:
                code = line.rstrip()
                print('#' * 75)
                print('Actual Rule: ', code)
                inputStream = InputStream(code)
                lexer = comparatorLexer(inputStream)
                stream = CommonTokenStream(lexer)
                parser = comparatorParser(stream)
                tree = parser.expression()
                print(tree.toStringTree(recog=parser))
                children = []
                for child in tree.getChildren():
                    children.append((child.getText()))
                print('*' * 50)
                print("All the parsed tokens: ", children)
                r_i = RuleInterpreter(children)
        return True
    except:
        return False


if __name__ == '__main__':
    main(sys.argv)
