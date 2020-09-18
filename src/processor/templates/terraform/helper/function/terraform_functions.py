from processor.templates.terraform.helper.function import collection_functions
from processor.templates.terraform.helper.function import numeric_functions
from processor.templates.terraform.helper.function import string_functions

default_functions = [
    # collection functions
    { "expression" : "(element[(].*[,].*[)])$", "method" : collection_functions.element },
    { "expression" : "(length[(].*[)])$", "method" : collection_functions.length },
    { "expression" : "(chunklist[(].*[)])$", "method" : collection_functions.chunklist },
    { "expression" : "(concat[(].*[)])$", "method" : collection_functions.concat },
    { "expression" : "(coalesce[(].*[)])$", "method" : collection_functions.coalesce },
    { "expression" : "(coalescelist[(].*[)])$", "method" : collection_functions.coalescelist },
    { "expression" : "(compact[(].*[)])$", "method" : collection_functions.compact },
    { "expression" : "(distinct[(].*[)])$", "method" : collection_functions.distinct },
    { "expression" : "(index[(].*[)])$", "method" : collection_functions.index },
    { "expression" : "(lookup[(].*[,].*[)])$", "method" : collection_functions.lookup },
    { "expression" : "(contains[(].*[,].*[)])$", "method" : collection_functions.contains },
    { "expression" : "(keys[(].*[)])$", "method" : collection_functions.keys },
    { "expression" : "(list[(].*[)])$", "method" : collection_functions.to_list },
    { "expression" : "(map[(].*[)])$", "method" : collection_functions.to_map },
    { "expression" : "(merge[(].*[)])$", "method" : collection_functions.merge },
    { "expression" : "(reverse[(].*[)])$", "method" : collection_functions.reverse },

    # numeric functions
    { "expression" : "(abs[(].*[)])$", "method" : numeric_functions.to_abs },
    { "expression" : "(ceil[(].*[)])$", "method" : numeric_functions.ceil },
    { "expression" : "(floor[(].*[)])$", "method" : numeric_functions.floor },
    { "expression" : "(log[(].*[)])$", "method" : numeric_functions.log },
    { "expression" : "(max[(].*[)])$", "method" : numeric_functions.to_max },
    { "expression" : "(min[(].*[)])$", "method" : numeric_functions.to_min },
    { "expression" : "(pow[(].*[)])$", "method" : numeric_functions.pow },
    { "expression" : "(signum[(].*[)])$", "method" : numeric_functions.signum },

    # string funtion
    { "expression" : "(chomp[(].*[)])$", "method" : string_functions.chomp },
    { "expression" : "(join[(].*[)])$", "method" : string_functions.join },
]