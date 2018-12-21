import sys
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from comparatorLexer import comparatorLexer
from comparatorParser import comparatorParser
from rule_interpreter import RuleInterpreter


def main(argv):
    # input = FileStream(argv[1])
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
            # print(tree.toStringTree(recog=parser))
            children = []
            for child in tree.getChildren():
                children.append((child.getText()))
            print('*' * 50)
            print("All the parsed tokens: ", children)
            r_i = RuleInterpreter(children)
            print('LHS operand: ', r_i.lhs)
            print('Comparator: ', r_i.op)
            print('RHS operand: ', r_i.rhs)
            print('!' * 50)
            # print(r_i.match_method(''.join(r_i.lhs)))
            # print(r_i.match_method(''.join(r_i.rhs)))
            r_i.compare()


if __name__ == '__main__':
    main(sys.argv)
