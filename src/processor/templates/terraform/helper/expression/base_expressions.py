"""
process the expression and returns the processed values
"""
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
    new_expression = '%s if %s else %s' % (true_value, condition, false_value)
    try:
        response = eval(new_expression)
        return response
    except Exception as e:
        logger.error(e)
        return expression