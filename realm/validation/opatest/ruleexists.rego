package rule
default rulepass = true
rulepass = false{
   is_null(input.SecurityGroups)
}
