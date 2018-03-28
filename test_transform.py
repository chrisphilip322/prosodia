#!/usr/bin/env python
import typing

import parser_v2 as p

S = typing.TypeVar('S')
T = typing.TypeVar('T')

class RequireType(object):
    def __init__(self, func: typing.Callable[[S], T]) -> None:
        self.func = func

    def __getitem__(self, explicit_type: type) -> typing.Callable[[S], T]:
        def double_wrapped(s: S) -> T:
            return self.func(s)

        double_wrapped.__annotations__['template_type'] = explicit_type
        double_wrapped.__annotations__['original_func'] = self.func
        return double_wrapped


def syntax_accum(
    values: typing.Tuple[typing.Sequence[p.Rule], None]
) -> p.Language:
    rules = values[0]
    lang = p.Language.create(rules[0].name)
    for rule in rules:
        lang.add_rule(rule)
    return lang

@RequireType
def list_of(
    values: typing.Tuple[T]
) -> typing.List[T]:
    return [values[0]]

@RequireType
def push_list(
    values: typing.Tuple[T, typing.List[T]]
) -> typing.List[T]:
    return [values[0]] + values[1]

lt = p.LanguageTransformation.create()
lt.add_rule_transformation(
    p.RuleTransformation(
        'Syntax',
        p.SyntaxTransformation.create(
            p.TermGroupTransformation(
                syntax_accum
            )
        )
    ),
)
lt.add_rule_transformation(
    p.RuleTransformation(
        'Rules',
        p.SyntaxTransformation.create(
            p.TermGroupTransformation(list_of[p.Rule]),
            p.TermGroupTransformation(push_list[p.Rule]),
        )
    )
)
