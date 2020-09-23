"""
Performs all in built string functions which are supported by terraform processor
"""
from processor.logging.log_handler import getlogger
import decimal

logger = getlogger()

def chomp(str_value):
    """ removes newline characters at the end of a string. """
    return str_value.rstrip()

# def format(str_value):
#     """ removes newline characters at the end of a string. """
#     return str_value.rstrip()
    
def join(concat_ele, ele_list):
    """ concat list items and returns a string """
    return concat_ele.join(ele_list)

def lower(str_value):
    """ convert string to lower case """
    return str_value.lower()

def replace(str_value, substring, replacement):
    """ searches for substring and replace the value of substring """
    return str_value.replace(substring , replacement)

def split(separator, str_value):
    """ split the string by given separator and returns the list """
    return str_value.split(separator) 

def trim(str_value, trim_string):
    """ trim the characters from the given string """
    return str_value.strip(trim_string)

def trimprefix(str_value, trim_string):
    """ trim the characters from the given string """
    if str_value.startswith(trim_string):
        str_value = str_value[len(trim_string):]
        return trimprefix(str_value, trim_string)
    return str_value

def trimsuffix(str_value, trim_string):
    """ trim the characters from the given string """
    if str_value.endswith(trim_string):
        str_value = str_value[:-(len(trim_string))]
        return trimsuffix(str_value, trim_string)
    return str_value

def trimspace(str_value):
    """ trim the space from the given string """
    return str_value.strip()
    
def upper(str_value):
    """ convert string to upper case """
    return str_value.upper()

def strrev(str_value):
    """ reverse the characters of given string """
    return str_value[::-1]

def substr(str_value, offset, length):
    """ return the subsctring of given string """
    return str_value[offset:length]

def title(str_value):
    """ converts the first character of each word of given string to uppercase. """
    return str_value.title()
    