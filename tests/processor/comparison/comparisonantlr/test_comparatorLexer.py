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


def test_comparatorParser():
    from antlr4 import InputStream
    from antlr4 import CommonTokenStream
    from processor.comparison.comparisonantlr.comparatorLexer import comparatorLexer
    from processor.comparison.comparisonantlr.comparatorParser import comparatorParser
    from processor.comparison.interpreter import RuleInterpreter
    vals = [
        'count({1}.firewall.rules[] + {2}.firewall.rules[]) = 13',
        'count({1}.firewall.rules[]) + count({2}.firewall.rules[]) = 13',
        'count({1}.firewall.rules[] + {2}.firewall.rules[]) > 13',
        'count({1}.firewall.rules[] + {2}.firewall.rules[]) < 13',
        'count({1}.firewall.rules[] + {2}.firewall.rules[]) >= 13',
        'count({1}.firewall.rules[] + {2}.firewall.rules[]) <= 13',
        'count({1}.firewall.rules[] + {2}.firewall.rules[]) != 13',
        'count({1}.firewall.rules[]) = count({2}.firewall.rules[])',
        "{2}.properties.cost=2.34",
        "{2}.properties.addressSpace={'addressPrefixes': ['172.18.116.0/23']}",
        "{1}.[0].name=abcd",
        "{1}.['name' = 'abcd'].location = 'eastus2'",
        '{1}.dns.ip = 1.2.4.5',
        '{1}.dns.ip = 1.2.4.5/32',
        '{1}.location = [1,2,4]',
        "{2}.properties.dhcpOptions.dnsServers[]+{3}.properties.dhcpOptions.dnsServers[]=['172.18.96.214', '172.18.96.216', '172.18.96.214', '172.18.96.216']",
        'count(count(count({1}.location.name[0]))+count(count({2}.location.name[0])))= 13',
        "{1}.firewall.rules['name' = 'rule1'].port = {2}.firewall.rules['name' = 'rule1'].port",
        'count({1}.firewall.rules[]) = count({2}.firewall.rules[])',
        'count(count({1}.firewall.rules[]) + count({1}.firewall.rules[])) = 13',
        'exist({1}.location)',
        'exist({1}.location) = TRUE',
        'exist({1}.location) = true',
        'exist({1}.location) = FALSE',
        'exist({1}.location) = false',
        'exist({1}[0].location)',
        'exist({1}.firewall.location)',
        'exist({1}.firewall.rules[])',
        'count({1}.firewall.rules[]) != 13',
        'count({1}.firewall.rules[]) = 13',
        '{1}.firewall.port = 443',
        "{1}.location = 'eastus2'",
        'exist({1}.location) = FAlSE',
        '{1}.firewall.port = 443',
        "{1}.firewall.rules['name' = 'rule1'].port = 443",
        "{1}.firewall.port = {2}.firewall.port",
        '{1}.firewall.rules[0].port = {2}.firewall.port',
        'exist({1}[0].location)',
        "exist({1}['name' = 'abc'])",
        "{1}.firewall.rules['name' = 'abc'].port = {2}.firewall.port",
        "{1}.firewall.rules['name' = 'abc'].ports[2].port = {2}.firewall.port",
        "{1}.firewall.cost = 443.25",
        "{1}[0].location = 'eastus2'",

    ]
    for line in vals:
        code = line.rstrip()
        # print('#' * 75)
        # print('Actual Rule: ', code)
        inputStream = InputStream(code)
        lexer = comparatorLexer(inputStream)
        stream = CommonTokenStream(lexer)
        parser = comparatorParser(stream)
        tree = parser.expression()
        # print(tree.toStringTree(recog=parser))
        children = []
        for child in tree.getChildren():
            children.append((child.getText()))
        assert len(children) > 0
        # print('*' * 50)
        # print("All the parsed tokens: ", children)
        r_i = RuleInterpreter(children)
        assert r_i is not None




