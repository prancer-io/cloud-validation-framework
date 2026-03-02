"""
process the expression and returns the processed values
"""
import ast
import operator
import re
from processor.logging.log_handler import getlogger

logger = getlogger()

# Supported comparison operators for condition evaluation
_COMPARISON_OPS = {
    "<=": operator.le,
    ">=": operator.ge,
    "!=": operator.ne,
    "==": operator.eq,
    "<": operator.lt,
    ">": operator.gt,
}

def _evaluate_condition(condition):
    """
    Evaluate a condition string that may contain comparison operators.
    Returns the boolean result of the condition.
    """
    # First try literal eval for simple true/false/numeric values
    try:
        return ast.literal_eval(condition)
    except (ValueError, SyntaxError):
        pass

    # Try to evaluate comparison expressions like "2 < 1", "0 >= 1", etc.
    for op_str, op_func in _COMPARISON_OPS.items():
        parts = condition.split(op_str)
        if len(parts) == 2:
            left, right = parts[0].strip(), parts[1].strip()
            try:
                left_val = ast.literal_eval(left)
                right_val = ast.literal_eval(right)
                return op_func(left_val, right_val)
            except (ValueError, SyntaxError):
                continue

    # Fallback: treat non-empty string as truthy
    return bool(condition)


def conditional_expression(expression):
    """
    perform the condition operation on provided expression and returns the result
    """
    expression_list = expression.split(" ? ", 1)
    condition = expression_list[0]
    rest = expression_list[1]
    true_value, false_value = rest.split(" : ", 1)
    try:
        ast.literal_eval(true_value)
    except (ValueError, SyntaxError):
        true_value = f'"{true_value}"'
    try:
        ast.literal_eval(false_value)
    except (ValueError, SyntaxError):
        false_value = f'"{false_value}"'
    condition_result = _evaluate_condition(condition)
    try:
        response = ast.literal_eval(true_value) if condition_result else ast.literal_eval(false_value)
        return response, True
    except Exception as e:
        logger.error(expression)
        logger.error(e)
        return expression, False
