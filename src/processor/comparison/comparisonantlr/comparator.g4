// The grammar for rule parsing, which shall be called comparator.
grammar comparator;

// All rule defined in the testcase be called as  expression
// could have called rule but has clashes with existing rule objects.
// It's a expression with expression, methodcall with or without comparison 
expression
    : (METHOD)? ('(')? (METHOD)? ('(')? FMT1 (')')? (OP (METHOD)? ('(')? FMT1 (')')?)* (')')? (COMP NUMBER|FNUMBER|BOOL|ARRSTRING|DICTSTRING)?
    | (METHOD)? ('(')? FMT1 (')')? (OP (METHOD)? ('(')? FMT1 (')')?)* (COMP (METHOD)? ('(')? FMT1 (OP FMT1)* (')')?)?
    | FMT1 (COMP NUMBER|FNUMBER)?
    | FMT1 (COMP IPADDRESS|STRING)?
    | FMT1 (COMP METHOD '(' FMT1 (OP FMT1)* ')')?
    | METHOD '(' FMT1 (OP FMT1)* ')' (COMP NUMBER|FNUMBER|BOOL)?
    | METHOD '(' FMT1 (OP FMT1)* ')' (COMP FMT1)?
    | METHOD '(' FMT1 (OP FMT1)* ')' (COMP STRING)?
    | METHOD '(' FMT1 (OP FMT1)* ')' (COMP METHOD '(' FMT1 (OP FMT1)* ')')?
    ;

// Define allowed method in the expression for comparison
METHOD
    : 'exist'
    | 'count'
    ;

BOOL
    : [Ff][Aa][Ll][Ss][Ee]
    | [Tt][Rr][Uu][Ee]
    ;

// Define operators between the expressions
OP
    : '+'
    ;

// Define comparisons for the expression to be compared against with
// the comparison operators.
COMP
    : '>'
    | '<'
    | '>='
    | '<='
    | '!='
    | '='
    ;

// Define the format of the expression to be parsed.
FMT1
    : '{' NUMBER '}' (('.' (ATTRFMT1|ATTRFMT2))|ATTRFMT3)+
    ;

// Define the attribute formats to access the objects.
ATTRFMT1
    : STRING ('['(NUMBER)?']')?
    ;

ATTRFMT2
    : STRING ('[' (QUOTE)? STRING (QUOTE)?  '=' (QUOTE)? STRING (QUOTE)?']')?
    ;

ATTRFMT3
    :'['(NUMBER | ((QUOTE)? STRING (QUOTE)?  '=' (QUOTE)? STRING (QUOTE)?))?']'
    ;


// The regular expression starts with a letter
// and may follow with any number of alphanumerical characters"
STRING
    : [a-zA-Z][a-zA-Z0-9_-]*
    ;

ARRSTRING
    : SQOPEN (IPADDRESS|QUOTESTRING) (',' (WS)* IPADDRESS|QUOTESTRING)* SQCLOSE;

DICTSTRING
    : FLOPEN (.)*? FLCLOSE;

QUOTESTRING
    : QUOTE STRING QUOTE
    ;

// Number format regular expression
NUMBER
    : [0-9]+
    ;

//Float Number format regular expression
FNUMBER
    : [0-9]+('.'[0-9]+)?
    ;

IPADDRESS : (QUOTE)?NUMBER '.' NUMBER '.' NUMBER '.' NUMBER ('/'NUMBER)?(QUOTE)?;

QUOTE : '\'';
SQOPEN : '[';
SQCLOSE : ']';
FLOPEN : '{';
FLCLOSE : '}';


// WS represents a whitespace, which is ignored entirely by skip.
WS
    : [ \t\u000C\r\n]+ -> skip
    ;
