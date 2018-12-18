import sys
from antlr4 import InputStream
from antlr4 import FileStream, CommonTokenStream
from comparatorLexer import comparatorLexer
from comparatorParser import comparatorParser


def main(argv):
    # input = FileStream(argv[1])
    with open(argv[1]) as f:
        for line in f:
            code = line.rstrip()
            print('#' * 75)
            print(code)
            inputStream = InputStream(code)
            lexer = comparatorLexer(inputStream)
            stream = CommonTokenStream(lexer)
            parser = comparatorParser(stream)
            tree = parser.expression()
            print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
