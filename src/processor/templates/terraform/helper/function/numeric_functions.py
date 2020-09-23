"""
performs all in built numeric functions which are supported by terraform processor
"""
from processor.logging.log_handler import getlogger
import math

def to_abs(num):
    """ return the absolute value of given number """
    return abs(num)

def ceil(num):
    """ return the smallest integer greater than or equal to given number """
    return math.ceil(num)

def floor(num):
    """ return the largest integer less than or equal to given number """
    return math.floor(num)

def log(num, base):
    """ returns the logarithm of a given number in a given base """
    return math.log(num, base)

def to_max(*args):
    """ returns the largest item from given list of items """
    return max(*args)

def to_min(*args):
    """ returns the smallest item from given list of items """
    return min(*args)

def pow(num, power):
    """ returns the number raised to the given power """
    return math.pow(num, power)

def signum(num):
    """ determines the sign of a number, returning a number between -1 and 1 """
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0