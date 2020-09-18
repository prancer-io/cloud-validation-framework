from processor.templates.terraform.helper.expression import base_expressions

expression_list = [
    { "expression" : "(^.*[?].*[:].*$)", "method" : base_expressions.conditional_expression },
]
