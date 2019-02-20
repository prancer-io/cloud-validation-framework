"""Utility functions"""

OK = 'OK'
NOK = 'NOK'
TOKENTIMEOUT = 60000
STATUS = 'status'
ERROR = 'error'
VALUE = 'value'
ADMIN = 'admin'
JSONMIME = 'application/json'
CONFIGFILE = 'config.json'


def gettokentimeout():
    "Return the token timeout"
    return TOKENTIMEOUT


def parseint(value, default=0):
    intvalue = default
    try:
        intvalue = int(value)
    except:
        pass
    return intvalue


def parsebool(val, defval=False):
    "Parse boolean from the input value"
    retval = defval
    if val:
        if isinstance(val, str) and val.lower() in ['false', 'true']:
            retval = True if val.lower() == 'true' else False
        else:
            retval = bool(parseint(val))
    return retval
#
#
# def get_integer_value(value, default=0):
#     "Parse integer from the string, otherwise return a default"
#     intvalue = default
#     try:
#         intvalue = int(value)
#     except:
#         pass
#     return intvalue
#
#
# def id_generator(size=6, chars=string.ascii_lowercase):
#     "Generate user id, regid and other random data as per the size and characters."
#     return ''.join(random.choice(chars) for _ in range(size))
#
#
# def get_default_datetime():
#     "Return current datetime object"
#     return datetime.datetime.now()
#
#
# def getIntegerValue(value, default=0):
#     intvalue = default
#     try:
#         intvalue = int(value)
#     except:
#         pass
#     return intvalue
#
#
#
# def getStringValue(value, default=None):
#     return value
#
#
# def parse_datetime(value):
#     try:
#         dateval = parser.parse(value, dayfirst=False)
#     except:
#         dateval = datetime.datetime.now()
#     return dateval
#
#