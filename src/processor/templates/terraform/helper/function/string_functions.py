"""
Performs all in built string functions which are supported by terraform processor
"""
from processor.logging.log_handler import getlogger

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

# def str_replace(str_value, substring, replacement):
#     """ searches for substring and replace the value of substring """
#     return str_value.replace(substring , replacement)

def str_split(separator, str_value):
    """ split the string by given separator and returns the list """
    return str_value.split(separator) 

# def trim(str_value, trim_string):
#     """ trim the characters from the given string """
#     return str_value.strip(trim_string)

# def trimprefix(str_value, trim_string):
#     """ trim the characters from the given string """
#     return str_value.lstrip(trim_string)

# def trimsuffix(str_value, trim_string):
#     """ trim the characters from the given string """
#     return str_value.rstrip(trim_string)

# def trimspace(str_value):
#     """ trim the space from the given string """
#     return str_value.strip()
    