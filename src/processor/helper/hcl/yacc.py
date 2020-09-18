import sys
import types
import os
import re
from ply.yacc import tab_module, PlyLogger, get_caller_module_dict, ParserReflect, YaccError, \
        LRTable, LRParser, VersionError, YaccSymbol, YaccProduction, error_count, call_errorfunc, \
        yaccdebug, debug_file
from ply import lex
from hcl.lexer import Lexer, text_type, _raise_error
from processor.logging.log_handler import getlogger

logger = getlogger()

parse = None

class TerraformLexer(Lexer):
        
    tokens = (
        'BOOL',
        'FLOAT',
        'NUMBER',
        'COMMA',
        'IDENTIFIER',
        'OUTER_STRING_IDENTIFIER',
        'STRING_IDENTIFIER',
        'EQUAL',
        'STRING',
        'ADD',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        'LEFTBRACE',
        'RIGHTBRACE',
        'LEFTBRACKET',
        'RIGHTBRACKET',
        'PERIOD',
        'EPLUS',
        'EMINUS',
        'LEFTPAREN',
        'RIGHTPAREN',
        'QMARK',
        'COLON',
        'ASTERISK_PERIOD',
        'GT',
        'LT',
        'EQ',
        'NE',
        'LE',
        'GE',
    )

    def t_OUTER_STRING_IDENTIFIER(self, t):
        # r'"(.*)"$'
        r'(?<!^)"(.*)"$'
        t.value = text_type(t.value)
        return t

    def t_STRING_IDENTIFIER(self, t):
        r'"(?:[^\\"]|\\.)*"'
        t.value = text_type(t.value)
        return t

    def t_string(self, t):
        # Start of a string
        r'\"'
        # abs_start is the absolute start of the string. We use this at the end
        # to know how many new lines we've consumed
        t.lexer.abs_start = t.lexer.lexpos
        # rel_pos is the begining of the unconsumed part of the string. It will
        # get modified when consuming escaped characters
        t.lexer.rel_pos = t.lexer.lexpos
        # The value of the consumed part of the string
        t.lexer.string_value = u''
        t.lexer.begin('string')

    # Strings
    def t_string_escapedchar(self, t):
        # If a quote or backslash is escaped, build up the string by ignoring
        # the escape character. Should this be done for other characters?
        r'(?<=\\)(\"|\\)'
        t.lexer.string_value += (
            t.lexer.lexdata[t.lexer.rel_pos : t.lexer.lexpos - 2] + t.value
        )
        t.lexer.rel_pos = t.lexer.lexpos
        pass

    def t_string_stringdollar(self, t):
        # Left brace preceeded by a dollar
        r'(?<=\$)\{'
        t.lexer.braces = 1
        t.lexer.begin('stringdollar')

    def t_string_ignoring(self, t):
        # Ignore everything except for a quote
        r'[^\"]'
        pass

    def t_string_STRING(self, t):
        # End of the string
        r'\"'
        t.value = (
            t.lexer.string_value + t.lexer.lexdata[t.lexer.rel_pos : t.lexer.lexpos - 1]
        )
        t.lexer.lineno += t.lexer.lexdata[t.lexer.abs_start : t.lexer.lexpos - 1].count(
            '\n'
        )
        t.lexer.begin('INITIAL')
        return t

    def t_string_eof(self, t):
        t.lexer.lineno += t.lexer.lexdata[t.lexer.abs_start : t.lexer.lexpos].count(
            '\n'
        )
        _raise_error(t, 'EOF before closing string quote')

    def t_stringdollar_dontcare(self, t):
        # Ignore everything except for braces
        r'[^\{\}]'
        pass

    def t_stringdollar_lbrace(self, t):
        r'\{'
        t.lexer.braces += 1

    def t_stringdollar_rbrace(self, t):
        r'\}'
        t.lexer.braces -= 1

        if t.lexer.braces == 0:
            # End of the dollar brace, back to the rest of the string
            t.lexer.begin('string')

    def t_stringdollar_eof(self, t):
        t.lexer.lineno += t.lexer.lexdata[t.lexer.abs_start : t.lexer.lexpos].count(
            '\n'
        )
        _raise_error(t, "EOF before closing '${}' expression")

    def _init_heredoc(self, t):
        t.lexer.here_start = t.lexer.lexpos

        if t.value.endswith('\r\n'):
            t.lexer.newline_chars = 2
        else:
            t.lexer.newline_chars = 1

        if t.lexer.is_tabbed:
            # Chop '<<-'
            chop = 3
        else:
            # Chop '<<'
            chop = 2

        t.lexer.here_identifier = t.value[chop : -t.lexer.newline_chars]
        # We consumed a newline in the regex so bump the counter
        t.lexer.lineno += 1

    def t_tabbedheredoc(self, t):
        r'<<-\S+\r?\n'
        t.lexer.is_tabbed = True
        self._init_heredoc(t)
        t.lexer.begin('tabbedheredoc')

    def t_heredoc(self, t):
        r'<<\S+\r?\n'
        t.lexer.is_tabbed = False
        self._init_heredoc(t)
        t.lexer.begin('heredoc')

    def _end_heredoc(self, t):
        if t.lexer.is_tabbed:
            # Strip leading tabs
            value = t.value.strip()
        else:
            value = t.value

        if value == t.lexer.here_identifier:
            # Handle case where identifier is on a line of its own. Need to
            # subtract the current line and the newline characters from
            # the previous line to get the endpos
            endpos = t.lexer.lexpos - (t.lexer.newline_chars + len(t.value))
        elif value.endswith(t.lexer.here_identifier):
            # Handle case where identifier is at the end of the line. Need to
            # subtract the identifier from to get the endpos
            endpos = t.lexer.lexpos - len(t.lexer.here_identifier)
        else:
            return

        entire_string = t.lexer.lexdata[t.lexer.here_start : endpos]

        if t.lexer.is_tabbed:
            # Get rid of any initial tabs, and remove any tabs preceded by
            # a new line
            chopped_starting_tabs = re.sub('^\t*', '', entire_string)
            t.value = re.sub('\n\t*', '\n', chopped_starting_tabs)
        else:
            t.value = entire_string

        t.lexer.lineno += t.lexer.lexdata[t.lexer.here_start : t.lexer.lexpos].count(
            '\n'
        )
        t.lexer.begin('INITIAL')
        return t

    def t_tabbedheredoc_STRING(self, t):
        r'^\t*.+?(?=\r?$)'
        return self._end_heredoc(t)

    def t_heredoc_STRING(self, t):
        r'^.+?(?=\r?$)'
        return self._end_heredoc(t)

    def t_heredoc_ignoring(self, t):
        r'.+|\n'
        pass

    def t_heredoc_eof(self, t):
        t.lexer.lineno += t.lexer.lexdata[t.lexer.here_start : t.lexer.lexpos].count(
            '\n'
        )
        _raise_error(t, 'EOF before closing heredoc')

    t_tabbedheredoc_ignoring = t_heredoc_ignoring
    t_tabbedheredoc_eof = t_heredoc_eof

    t_LEFTBRACE = r'\{'
    t_RIGHTBRACE = r'\}'
    t_LEFTBRACKET = r'\['
    t_RIGHTBRACKET = r'\]'
    t_LEFTPAREN = r'\('
    t_RIGHTPAREN = r'\)'

    def t_COMMENT(self, t):
        r'(\#|(//)).*'
        pass

    def t_MULTICOMMENT(self, t):
        r'/\*(.|\n)*?(\*/)'
        t.lexer.lineno += t.value.count('\n')
        pass

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t\r\f\v'

    t_EQUAL = r'(?<!=)=(?!=)'
    t_ADD = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'

    # Error handling rule
    def t_error(self, t):
        if t.value.startswith('/*'):
            _raise_error(t, 'EOF before closing multiline comment')
        elif t.value.startswith('*/'):
            _raise_error(t, "Found '*/' before start of multiline comment")
        elif t.value.startswith('/'):
            c = t.value[1]
            _raise_error(t, "Expected '//' for comment, got '/%s'" % c)
        elif t.value.startswith('<<'):
            _raise_error(t, "Heredoc must have a marker, e.g. '<<FOO'")
        elif t.value.startswith('<'):
            c = t.value[1]
            _raise_error(t, "Heredoc must start with '<<', got '<%s'" % c)
        else:
            _raise_error(t)

class TerraformLRParser(LRParser):
    def parseopt_notrack(self, input=None, lexer=None, debug=False, tracking=False, tokenfunc=None):
        #--! parseopt-notrack-start
        lookahead = None                         # Current lookahead symbol
        lookaheadstack = []                      # Stack of lookahead symbols
        actions = self.action                    # Local reference to action table (to avoid lookup on self.)
        goto    = self.goto                      # Local reference to goto table (to avoid lookup on self.)
        prod    = self.productions               # Local reference to production list (to avoid lookup on self.)
        defaulted_states = self.defaulted_states # Local reference to defaulted states
        pslice  = YaccProduction(None)           # Production object passed to grammar rules
        errorcount = 0                           # Used during error recovery


        # If no lexer was given, we will try to use the lex module
        if not lexer:
            from . import lex
            lexer = lex.lexer

        # Set up the lexer and parser objects on pslice
        pslice.lexer = lexer
        pslice.parser = self

        # If input was supplied, pass to lexer
        if input is not None:
            lexer.input(input)

        if tokenfunc is None:
            # Tokenize function
            get_token = lexer.token
        else:
            get_token = tokenfunc

        # Set the parser() token method (sometimes used in error recovery)
        self.token = get_token

        # Set up the state and symbol stacks

        statestack = []                # Stack of parsing states
        self.statestack = statestack
        symstack   = []                # Stack of grammar symbols
        self.symstack = symstack

        pslice.stack = symstack         # Put in the production
        errtoken   = None               # Err token

        # The start state is assumed to be (0,$end)

        statestack.append(0)
        sym = YaccSymbol()
        sym.type = '$end'
        symstack.append(sym)
        state = 0
        while True:
            # Get the next symbol on the input.  If a lookahead symbol
            # is already set, we just use that. Otherwise, we'll pull
            # the next token off of the lookaheadstack or from the lexer


            if state not in defaulted_states:
                if not lookahead:
                    if not lookaheadstack:
                        lookahead = get_token()     # Get the next token
                    else:
                        lookahead = lookaheadstack.pop()
                    if not lookahead:
                        lookahead = YaccSymbol()
                        lookahead.type = '$end'

                if lookahead.type == "OUTER_STRING_IDENTIFIER":
                    lookahead.type = "STRING_IDENTIFIER"

                # Check the action table
                ltype = lookahead.type
                t = actions[state].get(ltype)
            else:
                t = defaulted_states[state]

            if t is not None:
                if t > 0:
                    # shift a symbol on the stack
                    statestack.append(t)
                    state = t


                    symstack.append(lookahead)
                    lookahead = None

                    # Decrease error count on successful shift
                    if errorcount:
                        errorcount -= 1
                    continue

                if t < 0:
                    # reduce a symbol on the stack, emit a production
                    p = prod[-t]
                    pname = p.name
                    plen  = p.len

                    # Get production function
                    sym = YaccSymbol()
                    sym.type = pname       # Production name
                    sym.value = None


                    if plen:
                        targ = symstack[-plen-1:]
                        targ[0] = sym


                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # The code enclosed in this section is duplicated
                        # below as a performance optimization.  Make sure
                        # changes get made in both locations.

                        pslice.slice = targ

                        try:
                            # Call the grammar rule with our special slice object
                            del symstack[-plen:]
                            self.state = state
                            p.callable(pslice)
                            del statestack[-plen:]
                            symstack.append(sym)
                            state = goto[statestack[-1]][pname]
                            statestack.append(state)
                        except SyntaxError:
                            # If an error was set. Enter error recovery state
                            lookaheadstack.append(lookahead)    # Save the current lookahead token
                            symstack.extend(targ[1:-1])         # Put the production slice back on the stack
                            statestack.pop()                    # Pop back one state (before the reduce)
                            state = statestack[-1]
                            sym.type = 'error'
                            sym.value = 'error'
                            lookahead = sym
                            errorcount = error_count
                            self.errorok = False

                        continue
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    else:


                        targ = [sym]

                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # The code enclosed in this section is duplicated
                        # above as a performance optimization.  Make sure
                        # changes get made in both locations.

                        pslice.slice = targ

                        try:
                            # Call the grammar rule with our special slice object
                            self.state = state
                            p.callable(pslice)
                            symstack.append(sym)
                            state = goto[statestack[-1]][pname]
                            statestack.append(state)
                        except SyntaxError:
                            # If an error was set. Enter error recovery state
                            lookaheadstack.append(lookahead)    # Save the current lookahead token
                            statestack.pop()                    # Pop back one state (before the reduce)
                            state = statestack[-1]
                            sym.type = 'error'
                            sym.value = 'error'
                            lookahead = sym
                            errorcount = error_count
                            self.errorok = False

                        continue
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if t == 0:
                    n = symstack[-1]
                    result = getattr(n, 'value', None)
                    return result

            if t is None:


                # We have some kind of parsing error here.  To handle
                # this, we are going to push the current token onto
                # the tokenstack and replace it with an 'error' token.
                # If there are any synchronization rules, they may
                # catch it.
                #
                # In addition to pushing the error token, we call call
                # the user defined p_error() function if this is the
                # first syntax error.  This function is only called if
                # errorcount == 0.
                if errorcount == 0 or self.errorok:
                    errorcount = error_count
                    self.errorok = False
                    errtoken = lookahead
                    if errtoken.type == '$end':
                        errtoken = None               # End of file!
                    if self.errorfunc:
                        if errtoken and not hasattr(errtoken, 'lexer'):
                            errtoken.lexer = lexer
                        self.state = state
                        tok = call_errorfunc(self.errorfunc, errtoken, self)
                        if self.errorok:
                            # User must have done some kind of panic
                            # mode recovery on their own.  The
                            # returned token is the next lookahead
                            lookahead = tok
                            errtoken = None
                            continue
                    else:
                        if errtoken:
                            if hasattr(errtoken, 'lineno'):
                                lineno = lookahead.lineno
                            else:
                                lineno = 0
                            if lineno:
                                sys.stderr.write('yacc: Syntax error at line %d, token=%s\n' % (lineno, errtoken.type))
                            else:
                                sys.stderr.write('yacc: Syntax error, token=%s' % errtoken.type)
                        else:
                            sys.stderr.write('yacc: Parse error in input. EOF\n')
                            return

                else:
                    errorcount = error_count

                # case 1:  the statestack only has 1 entry on it.  If we're in this state, the
                # entire parse has been rolled back and we're completely hosed.   The token is
                # discarded and we just keep going.

                if len(statestack) <= 1 and lookahead.type != '$end':
                    lookahead = None
                    errtoken = None
                    state = 0
                    # Nuke the pushback stack
                    del lookaheadstack[:]
                    continue

                # case 2: the statestack has a couple of entries on it, but we're
                # at the end of the file. nuke the top entry and generate an error token

                # Start nuking entries on the stack
                if lookahead.type == '$end':
                    # Whoa. We're really hosed here. Bail out
                    return

                if lookahead.type != 'error':
                    sym = symstack[-1]
                    if sym.type == 'error':
                        # Hmmm. Error is on top of stack, we'll just nuke input
                        # symbol and continue
                        lookahead = None
                        continue

                    # Create the error symbol for the first time and make it the new lookahead symbol
                    t = YaccSymbol()
                    t.type = 'error'

                    if hasattr(lookahead, 'lineno'):
                        t.lineno = t.endlineno = lookahead.lineno
                    if hasattr(lookahead, 'lexpos'):
                        t.lexpos = t.endlexpos = lookahead.lexpos
                    t.value = lookahead
                    lookaheadstack.append(lookahead)
                    lookahead = t
                else:
                    sym = symstack.pop()
                    statestack.pop()
                    state = statestack[-1]

                continue

            # Call an error function here
            raise RuntimeError('yacc: internal parser error!!!\n')

        #--! parseopt-notrack-end


def yacc(method='LALR', debug=yaccdebug, module=None, tabmodule=tab_module, start=None,
         check_recursion=True, optimize=False, write_tables=True, debugfile=debug_file,
         outputdir=None, debuglog=None, errorlog=None, picklefile=None):

    if tabmodule is None:
        tabmodule = tab_module

    # Reference to the parsing method of the last built parser
    global parse

    # If pickling is enabled, table files are not created
    if picklefile:
        write_tables = 0

    if errorlog is None:
        errorlog = PlyLogger(sys.stderr)

    # Get the module dictionary used for the parser
    if module:
        _items = [(k, getattr(module, k)) for k in dir(module)]
        pdict = dict(_items)
        if '__file__' not in pdict:
            pdict['__file__'] = sys.modules[pdict['__module__']].__file__
    else:
        pdict = get_caller_module_dict(2)

    if outputdir is None:
        if isinstance(tabmodule, types.ModuleType):
            srcfile = tabmodule.__file__
        else:
            if '.' not in tabmodule:
                srcfile = pdict['__file__']
            else:
                parts = tabmodule.split('.')
                pkgname = '.'.join(parts[:-1])
                exec('import %s' % pkgname)
                srcfile = getattr(sys.modules[pkgname], '__file__', '')
        outputdir = os.path.dirname(srcfile)

    pkg = pdict.get('__package__')
    if pkg and isinstance(tabmodule, str):
        if '.' not in tabmodule:
            tabmodule = pkg + '.' + tabmodule

    if start is not None:
        pdict['start'] = start

    pinfo = ParserReflect(pdict, log=errorlog)
    pinfo.get_all()

    if pinfo.error:
        raise YaccError('Unable to build parser')

    signature = pinfo.signature()

    # Read the tables
    try:
        lr = LRTable()
        if picklefile:
            read_signature = lr.read_pickle(picklefile)
        else:
            read_signature = lr.read_table(tabmodule)
        if optimize or (read_signature == signature):
            try:
                lr.bind_callables(pinfo.pdict)
                parser = TerraformLRParser(lr, pinfo.error_func)
                parse = parser.parse
                return parser
            except Exception as e:
                errorlog.warning('There was a problem loading the table file: %r', e)
    except VersionError as e:
        errorlog.warning(str(e))
    except ImportError:
        pass
