#!/usr/bin/env python

import parser_v2 as p

lt = p.LanguageTransformation.create()
lt.add_rule_transformation(
    p.RuleTransformation(
        'Syntax',
        ...
    )
)
