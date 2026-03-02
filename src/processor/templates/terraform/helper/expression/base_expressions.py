"""
process the expression and returns the processed values
"""
import ast
from processor.logging.log_handler import getlogger

logger = getlogger()


def conditional_expression(expression):
    """
    perform the condition operation on provided expression and returns the result
    """
    expression_list = expression.split(" ? ")
    condition = expression_list[0]
    true_value = expression_list[1].split(" : ")[0]
    false_value = expression_list[1].split(" : ")[1]
    try:
        ast.literal_eval(true_value)
    except (ValueError, SyntaxError):
        true_value = f'"{true_value}"'
    try:
        ast.literal_eval(false_value)
    except (ValueError, SyntaxError):
        false_value = f'"{false_value}"'
    try:
        condition_result = ast.literal_eval(condition)
    except (ValueError, SyntaxError):
        condition_result = bool(condition)
    try:
        response = ast.literal_eval(true_value) if condition_result else ast.literal_eval(false_value)
        return response, True
    except Exception as e:
        logger.error(expression)
        logger.error(e)
        return expression, False
