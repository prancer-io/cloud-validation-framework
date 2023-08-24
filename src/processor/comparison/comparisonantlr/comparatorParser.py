# Generated from comparator.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,24,194,2,0,7,0,1,0,3,0,4,8,0,1,0,3,0,7,8,0,1,0,3,0,10,8,0,1,
        0,3,0,13,8,0,1,0,1,0,3,0,17,8,0,1,0,1,0,3,0,21,8,0,1,0,3,0,24,8,
        0,1,0,1,0,3,0,28,8,0,5,0,30,8,0,10,0,12,0,33,9,0,1,0,3,0,36,8,0,
        1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,45,8,0,1,0,3,0,48,8,0,1,0,3,0,51,
        8,0,1,0,1,0,3,0,55,8,0,1,0,1,0,3,0,59,8,0,1,0,3,0,62,8,0,1,0,1,0,
        3,0,66,8,0,5,0,68,8,0,10,0,12,0,71,9,0,1,0,1,0,3,0,75,8,0,1,0,3,
        0,78,8,0,1,0,1,0,1,0,5,0,83,8,0,10,0,12,0,86,9,0,1,0,3,0,89,8,0,
        3,0,91,8,0,1,0,1,0,1,0,1,0,3,0,97,8,0,1,0,1,0,1,0,1,0,3,0,103,8,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,112,8,0,10,0,12,0,115,9,0,1,0,
        3,0,118,8,0,1,0,1,0,1,0,1,0,1,0,5,0,125,8,0,10,0,12,0,128,9,0,1,
        0,1,0,1,0,1,0,1,0,3,0,135,8,0,1,0,1,0,1,0,1,0,1,0,5,0,142,8,0,10,
        0,12,0,145,9,0,1,0,1,0,1,0,3,0,150,8,0,1,0,1,0,1,0,1,0,1,0,5,0,157,
        8,0,10,0,12,0,160,9,0,1,0,1,0,1,0,3,0,165,8,0,1,0,1,0,1,0,1,0,1,
        0,5,0,172,8,0,10,0,12,0,175,9,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,
        184,8,0,10,0,12,0,187,9,0,1,0,3,0,190,8,0,3,0,192,8,0,1,0,0,0,1,
        0,0,0,245,0,191,1,0,0,0,2,4,5,3,0,0,3,2,1,0,0,0,3,4,1,0,0,0,4,6,
        1,0,0,0,5,7,5,1,0,0,6,5,1,0,0,0,6,7,1,0,0,0,7,9,1,0,0,0,8,10,5,3,
        0,0,9,8,1,0,0,0,9,10,1,0,0,0,10,12,1,0,0,0,11,13,5,1,0,0,12,11,1,
        0,0,0,12,13,1,0,0,0,13,14,1,0,0,0,14,16,5,7,0,0,15,17,5,2,0,0,16,
        15,1,0,0,0,16,17,1,0,0,0,17,31,1,0,0,0,18,20,5,5,0,0,19,21,5,3,0,
        0,20,19,1,0,0,0,20,21,1,0,0,0,21,23,1,0,0,0,22,24,5,1,0,0,23,22,
        1,0,0,0,23,24,1,0,0,0,24,25,1,0,0,0,25,27,5,7,0,0,26,28,5,2,0,0,
        27,26,1,0,0,0,27,28,1,0,0,0,28,30,1,0,0,0,29,18,1,0,0,0,30,33,1,
        0,0,0,31,29,1,0,0,0,31,32,1,0,0,0,32,35,1,0,0,0,33,31,1,0,0,0,34,
        36,5,2,0,0,35,34,1,0,0,0,35,36,1,0,0,0,36,44,1,0,0,0,37,38,5,6,0,
        0,38,45,5,15,0,0,39,45,5,16,0,0,40,45,5,4,0,0,41,45,5,11,0,0,42,
        45,5,12,0,0,43,45,5,13,0,0,44,37,1,0,0,0,44,39,1,0,0,0,44,40,1,0,
        0,0,44,41,1,0,0,0,44,42,1,0,0,0,44,43,1,0,0,0,44,45,1,0,0,0,45,192,
        1,0,0,0,46,48,5,3,0,0,47,46,1,0,0,0,47,48,1,0,0,0,48,50,1,0,0,0,
        49,51,5,1,0,0,50,49,1,0,0,0,50,51,1,0,0,0,51,52,1,0,0,0,52,54,5,
        7,0,0,53,55,5,2,0,0,54,53,1,0,0,0,54,55,1,0,0,0,55,69,1,0,0,0,56,
        58,5,5,0,0,57,59,5,3,0,0,58,57,1,0,0,0,58,59,1,0,0,0,59,61,1,0,0,
        0,60,62,5,1,0,0,61,60,1,0,0,0,61,62,1,0,0,0,62,63,1,0,0,0,63,65,
        5,7,0,0,64,66,5,2,0,0,65,64,1,0,0,0,65,66,1,0,0,0,66,68,1,0,0,0,
        67,56,1,0,0,0,68,71,1,0,0,0,69,67,1,0,0,0,69,70,1,0,0,0,70,90,1,
        0,0,0,71,69,1,0,0,0,72,74,5,6,0,0,73,75,5,3,0,0,74,73,1,0,0,0,74,
        75,1,0,0,0,75,77,1,0,0,0,76,78,5,1,0,0,77,76,1,0,0,0,77,78,1,0,0,
        0,78,79,1,0,0,0,79,84,5,7,0,0,80,81,5,5,0,0,81,83,5,7,0,0,82,80,
        1,0,0,0,83,86,1,0,0,0,84,82,1,0,0,0,84,85,1,0,0,0,85,88,1,0,0,0,
        86,84,1,0,0,0,87,89,5,2,0,0,88,87,1,0,0,0,88,89,1,0,0,0,89,91,1,
        0,0,0,90,72,1,0,0,0,90,91,1,0,0,0,91,192,1,0,0,0,92,96,5,7,0,0,93,
        94,5,6,0,0,94,97,5,15,0,0,95,97,5,16,0,0,96,93,1,0,0,0,96,95,1,0,
        0,0,96,97,1,0,0,0,97,192,1,0,0,0,98,102,5,7,0,0,99,100,5,6,0,0,100,
        103,5,17,0,0,101,103,5,11,0,0,102,99,1,0,0,0,102,101,1,0,0,0,102,
        103,1,0,0,0,103,192,1,0,0,0,104,117,5,7,0,0,105,106,5,6,0,0,106,
        107,5,3,0,0,107,108,5,1,0,0,108,113,5,7,0,0,109,110,5,5,0,0,110,
        112,5,7,0,0,111,109,1,0,0,0,112,115,1,0,0,0,113,111,1,0,0,0,113,
        114,1,0,0,0,114,116,1,0,0,0,115,113,1,0,0,0,116,118,5,2,0,0,117,
        105,1,0,0,0,117,118,1,0,0,0,118,192,1,0,0,0,119,120,5,3,0,0,120,
        121,5,1,0,0,121,126,5,7,0,0,122,123,5,5,0,0,123,125,5,7,0,0,124,
        122,1,0,0,0,125,128,1,0,0,0,126,124,1,0,0,0,126,127,1,0,0,0,127,
        129,1,0,0,0,128,126,1,0,0,0,129,134,5,2,0,0,130,131,5,6,0,0,131,
        135,5,15,0,0,132,135,5,16,0,0,133,135,5,4,0,0,134,130,1,0,0,0,134,
        132,1,0,0,0,134,133,1,0,0,0,134,135,1,0,0,0,135,192,1,0,0,0,136,
        137,5,3,0,0,137,138,5,1,0,0,138,143,5,7,0,0,139,140,5,5,0,0,140,
        142,5,7,0,0,141,139,1,0,0,0,142,145,1,0,0,0,143,141,1,0,0,0,143,
        144,1,0,0,0,144,146,1,0,0,0,145,143,1,0,0,0,146,149,5,2,0,0,147,
        148,5,6,0,0,148,150,5,7,0,0,149,147,1,0,0,0,149,150,1,0,0,0,150,
        192,1,0,0,0,151,152,5,3,0,0,152,153,5,1,0,0,153,158,5,7,0,0,154,
        155,5,5,0,0,155,157,5,7,0,0,156,154,1,0,0,0,157,160,1,0,0,0,158,
        156,1,0,0,0,158,159,1,0,0,0,159,161,1,0,0,0,160,158,1,0,0,0,161,
        164,5,2,0,0,162,163,5,6,0,0,163,165,5,11,0,0,164,162,1,0,0,0,164,
        165,1,0,0,0,165,192,1,0,0,0,166,167,5,3,0,0,167,168,5,1,0,0,168,
        173,5,7,0,0,169,170,5,5,0,0,170,172,5,7,0,0,171,169,1,0,0,0,172,
        175,1,0,0,0,173,171,1,0,0,0,173,174,1,0,0,0,174,176,1,0,0,0,175,
        173,1,0,0,0,176,189,5,2,0,0,177,178,5,6,0,0,178,179,5,3,0,0,179,
        180,5,1,0,0,180,185,5,7,0,0,181,182,5,5,0,0,182,184,5,7,0,0,183,
        181,1,0,0,0,184,187,1,0,0,0,185,183,1,0,0,0,185,186,1,0,0,0,186,
        188,1,0,0,0,187,185,1,0,0,0,188,190,5,2,0,0,189,177,1,0,0,0,189,
        190,1,0,0,0,190,192,1,0,0,0,191,3,1,0,0,0,191,47,1,0,0,0,191,92,
        1,0,0,0,191,98,1,0,0,0,191,104,1,0,0,0,191,119,1,0,0,0,191,136,1,
        0,0,0,191,151,1,0,0,0,191,166,1,0,0,0,192,1,1,0,0,0,37,3,6,9,12,
        16,20,23,27,31,35,44,47,50,54,58,61,65,69,74,77,84,88,90,96,102,
        113,117,126,134,143,149,158,164,173,185,189,191
    ]

class comparatorParser ( Parser ):

    grammarFileName = "comparator.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "<INVALID>", "<INVALID>", 
                     "'+'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'*'", "'['", "']'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "METHOD", "BOOL", 
                      "OP", "COMP", "FMT1", "ATTRFMT1", "ATTRFMT2", "ATTRFMT3", 
                      "STRING", "ARRSTRING", "DICTSTRING", "QUOTESTRING", 
                      "NUMBER", "FNUMBER", "IPADDRESS", "QUOTE", "STAR", 
                      "SQOPEN", "SQCLOSE", "FLOPEN", "FLCLOSE", "WS" ]

    RULE_expression = 0

    ruleNames =  [ "expression" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    METHOD=3
    BOOL=4
    OP=5
    COMP=6
    FMT1=7
    ATTRFMT1=8
    ATTRFMT2=9
    ATTRFMT3=10
    STRING=11
    ARRSTRING=12
    DICTSTRING=13
    QUOTESTRING=14
    NUMBER=15
    FNUMBER=16
    IPADDRESS=17
    QUOTE=18
    STAR=19
    SQOPEN=20
    SQCLOSE=21
    FLOPEN=22
    FLCLOSE=23
    WS=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FMT1(self, i:int=None):
            if i is None:
                return self.getTokens(comparatorParser.FMT1)
            else:
                return self.getToken(comparatorParser.FMT1, i)

        def METHOD(self, i:int=None):
            if i is None:
                return self.getTokens(comparatorParser.METHOD)
            else:
                return self.getToken(comparatorParser.METHOD, i)

        def OP(self, i:int=None):
            if i is None:
                return self.getTokens(comparatorParser.OP)
            else:
                return self.getToken(comparatorParser.OP, i)

        def COMP(self):
            return self.getToken(comparatorParser.COMP, 0)

        def NUMBER(self):
            return self.getToken(comparatorParser.NUMBER, 0)

        def FNUMBER(self):
            return self.getToken(comparatorParser.FNUMBER, 0)

        def BOOL(self):
            return self.getToken(comparatorParser.BOOL, 0)

        def STRING(self):
            return self.getToken(comparatorParser.STRING, 0)

        def ARRSTRING(self):
            return self.getToken(comparatorParser.ARRSTRING, 0)

        def DICTSTRING(self):
            return self.getToken(comparatorParser.DICTSTRING, 0)

        def IPADDRESS(self):
            return self.getToken(comparatorParser.IPADDRESS, 0)

        def getRuleIndex(self):
            return comparatorParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)




    def expression(self):

        localctx = comparatorParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.state = 191
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 3
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 2
                    self.match(comparatorParser.METHOD)


                self.state = 6
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 5
                    self.match(comparatorParser.T__0)


                self.state = 9
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 8
                    self.match(comparatorParser.METHOD)


                self.state = 12
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 11
                    self.match(comparatorParser.T__0)


                self.state = 14
                self.match(comparatorParser.FMT1)
                self.state = 16
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                if la_ == 1:
                    self.state = 15
                    self.match(comparatorParser.T__1)


                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 18
                    self.match(comparatorParser.OP)
                    self.state = 20
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==3:
                        self.state = 19
                        self.match(comparatorParser.METHOD)


                    self.state = 23
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==1:
                        self.state = 22
                        self.match(comparatorParser.T__0)


                    self.state = 25
                    self.match(comparatorParser.FMT1)
                    self.state = 27
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                    if la_ == 1:
                        self.state = 26
                        self.match(comparatorParser.T__1)


                    self.state = 33
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 34
                    self.match(comparatorParser.T__1)


                self.state = 44
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [6]:
                    self.state = 37
                    self.match(comparatorParser.COMP)
                    self.state = 38
                    self.match(comparatorParser.NUMBER)
                    pass
                elif token in [16]:
                    self.state = 39
                    self.match(comparatorParser.FNUMBER)
                    pass
                elif token in [4]:
                    self.state = 40
                    self.match(comparatorParser.BOOL)
                    pass
                elif token in [11]:
                    self.state = 41
                    self.match(comparatorParser.STRING)
                    pass
                elif token in [12]:
                    self.state = 42
                    self.match(comparatorParser.ARRSTRING)
                    pass
                elif token in [13]:
                    self.state = 43
                    self.match(comparatorParser.DICTSTRING)
                    pass
                elif token in [-1]:
                    pass
                else:
                    pass
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 46
                    self.match(comparatorParser.METHOD)


                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 49
                    self.match(comparatorParser.T__0)


                self.state = 52
                self.match(comparatorParser.FMT1)
                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 53
                    self.match(comparatorParser.T__1)


                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 56
                    self.match(comparatorParser.OP)
                    self.state = 58
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==3:
                        self.state = 57
                        self.match(comparatorParser.METHOD)


                    self.state = 61
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==1:
                        self.state = 60
                        self.match(comparatorParser.T__0)


                    self.state = 63
                    self.match(comparatorParser.FMT1)
                    self.state = 65
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==2:
                        self.state = 64
                        self.match(comparatorParser.T__1)


                    self.state = 71
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 90
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 72
                    self.match(comparatorParser.COMP)
                    self.state = 74
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==3:
                        self.state = 73
                        self.match(comparatorParser.METHOD)


                    self.state = 77
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==1:
                        self.state = 76
                        self.match(comparatorParser.T__0)


                    self.state = 79
                    self.match(comparatorParser.FMT1)
                    self.state = 84
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==5:
                        self.state = 80
                        self.match(comparatorParser.OP)
                        self.state = 81
                        self.match(comparatorParser.FMT1)
                        self.state = 86
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 88
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==2:
                        self.state = 87
                        self.match(comparatorParser.T__1)




                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 92
                self.match(comparatorParser.FMT1)
                self.state = 96
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [6]:
                    self.state = 93
                    self.match(comparatorParser.COMP)
                    self.state = 94
                    self.match(comparatorParser.NUMBER)
                    pass
                elif token in [16]:
                    self.state = 95
                    self.match(comparatorParser.FNUMBER)
                    pass
                elif token in [-1]:
                    pass
                else:
                    pass
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 98
                self.match(comparatorParser.FMT1)
                self.state = 102
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [6]:
                    self.state = 99
                    self.match(comparatorParser.COMP)
                    self.state = 100
                    self.match(comparatorParser.IPADDRESS)
                    pass
                elif token in [11]:
                    self.state = 101
                    self.match(comparatorParser.STRING)
                    pass
                elif token in [-1]:
                    pass
                else:
                    pass
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 104
                self.match(comparatorParser.FMT1)
                self.state = 117
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 105
                    self.match(comparatorParser.COMP)
                    self.state = 106
                    self.match(comparatorParser.METHOD)
                    self.state = 107
                    self.match(comparatorParser.T__0)
                    self.state = 108
                    self.match(comparatorParser.FMT1)
                    self.state = 113
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==5:
                        self.state = 109
                        self.match(comparatorParser.OP)
                        self.state = 110
                        self.match(comparatorParser.FMT1)
                        self.state = 115
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 116
                    self.match(comparatorParser.T__1)


                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 119
                self.match(comparatorParser.METHOD)
                self.state = 120
                self.match(comparatorParser.T__0)
                self.state = 121
                self.match(comparatorParser.FMT1)
                self.state = 126
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 122
                    self.match(comparatorParser.OP)
                    self.state = 123
                    self.match(comparatorParser.FMT1)
                    self.state = 128
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 129
                self.match(comparatorParser.T__1)
                self.state = 134
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [6]:
                    self.state = 130
                    self.match(comparatorParser.COMP)
                    self.state = 131
                    self.match(comparatorParser.NUMBER)
                    pass
                elif token in [16]:
                    self.state = 132
                    self.match(comparatorParser.FNUMBER)
                    pass
                elif token in [4]:
                    self.state = 133
                    self.match(comparatorParser.BOOL)
                    pass
                elif token in [-1]:
                    pass
                else:
                    pass
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 136
                self.match(comparatorParser.METHOD)
                self.state = 137
                self.match(comparatorParser.T__0)
                self.state = 138
                self.match(comparatorParser.FMT1)
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 139
                    self.match(comparatorParser.OP)
                    self.state = 140
                    self.match(comparatorParser.FMT1)
                    self.state = 145
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 146
                self.match(comparatorParser.T__1)
                self.state = 149
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 147
                    self.match(comparatorParser.COMP)
                    self.state = 148
                    self.match(comparatorParser.FMT1)


                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 151
                self.match(comparatorParser.METHOD)
                self.state = 152
                self.match(comparatorParser.T__0)
                self.state = 153
                self.match(comparatorParser.FMT1)
                self.state = 158
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 154
                    self.match(comparatorParser.OP)
                    self.state = 155
                    self.match(comparatorParser.FMT1)
                    self.state = 160
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 161
                self.match(comparatorParser.T__1)
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 162
                    self.match(comparatorParser.COMP)
                    self.state = 163
                    self.match(comparatorParser.STRING)


                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 166
                self.match(comparatorParser.METHOD)
                self.state = 167
                self.match(comparatorParser.T__0)
                self.state = 168
                self.match(comparatorParser.FMT1)
                self.state = 173
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 169
                    self.match(comparatorParser.OP)
                    self.state = 170
                    self.match(comparatorParser.FMT1)
                    self.state = 175
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 176
                self.match(comparatorParser.T__1)
                self.state = 189
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 177
                    self.match(comparatorParser.COMP)
                    self.state = 178
                    self.match(comparatorParser.METHOD)
                    self.state = 179
                    self.match(comparatorParser.T__0)
                    self.state = 180
                    self.match(comparatorParser.FMT1)
                    self.state = 185
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==5:
                        self.state = 181
                        self.match(comparatorParser.OP)
                        self.state = 182
                        self.match(comparatorParser.FMT1)
                        self.state = 187
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 188
                    self.match(comparatorParser.T__1)


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




