#!/usr/bin/env python
import typing

import parser_v2 as p
from validate_transform_types import TypeAdder
from parse_bnf import ALLOWED_SYMBOLS

S = typing.TypeVar('S')
T = typing.TypeVar('T')

def syntax_accum(
    values: typing.Tuple[typing.Sequence[p.Rule], None]
) -> p.Language:
    rules = values[0]
    lang = p.Language.create(rules[0].name)
    eol_rule = p.Rule(
        'EOL',
        p.Syntax.create(
            p.TermGroup.create(
                p.Literal('\n')
            )
        )
    )
    eof_rule = p.Rule(
        'EOF',
        p.Syntax.create(
            p.TermGroup.create(
                p.EOFTerm()
            )
        )
    )
    lang.add_rule(eol_rule)
    lang.add_rule(eof_rule)
    for rule in rules:
        lang.add_rule(rule)
    return lang

def rule_accum(
    values: typing.Tuple[
        None,
        str,
        p.RuleName,
        str,
        None,
        str,
        None,
        typing.Sequence[p.TermGroup],
        None
    ]
) -> p.Rule:
    return p.Rule(values[2], p.Syntax(values[7]))

def expression_accum(
    values: typing.Tuple[
        p.TermGroup,
        None,
        str,
        None,
        typing.Sequence[p.TermGroup]
    ]
) -> typing.Sequence[p.TermGroup]:
    return [values[0]] + values[4]

def list_accum_1(
    values: typing.Tuple[p.Term]
) -> p.TermGroup:
    return p.TermGroup(list(values))

def list_accum_2(
    values: typing.Tuple[p.Term, None, p.TermGroup]
) -> p.TermGroup:
    return p.TermGroup([values[0]] + values[2].terms)

def text_accum_1(
    values: typing.Tuple[str]
) -> p.Literal:
    return p.Literal(values[0])

def text_accum_2(
    values: typing.Tuple[str, p.Literal]
) -> p.Literal:
    return p.Literal(values[0] + values[1].text)

def term_accum_rule(
    values: typing.Tuple[str, p.RuleName, str]
) -> p.RuleReference:
    return p.RuleReference(values[1])

@TypeAdder
def list_of(
    values: typing.Tuple[T]
) -> typing.List[T]:
    return [values[0]]

@TypeAdder
def push_list(
    values: typing.Tuple[T, typing.List[T]]
) -> typing.List[T]:
    return [values[0]] + values[1]

@TypeAdder
def nothing(_: typing.Tuple) -> None:
    return None

@TypeAdder
def identity(values: typing.Tuple[T]) -> T:
    return values[0]

@TypeAdder
def unescape(
    values: typing.Tuple[str, T, str]
) -> T:
    return values[1]

@TypeAdder
def add(
    values: typing.Tuple[T, ...]
) -> T:
    iterable = iter(values)
    accum = next(iterable)
    for item in iterable:
        accum += item
    return accum


lt = p.LanguageTransformation.create()
lt <<= 'Syntax', [syntax_accum]
lt <<= 'Rules', [
    list_of[[p.Rule], typing.Sequence[p.Rule]],
    push_list[[p.Rule, typing.Sequence[p.Rule]], typing.Sequence[p.Rule]]
]
lt <<= 'Rule', [rule_accum]
lt <<= 'OptWhitespace', [
    nothing[[str, None], None],
    nothing[[str], None]
]
lt <<= 'Expression', [
    list_of[[p.TermGroup], typing.Sequence[p.TermGroup]],
    expression_accum
]
lt <<= 'LineEnd', [
    nothing[[None], None],
    nothing[[None, None], None],
]
lt <<= 'SingleLineEnd', [
    nothing[[None, str], None]
]
lt <<= 'List', [
    list_accum_1,
    list_accum_2
]
lt <<= 'Term', [
    identity[[p.Literal], p.Literal],
    term_accum_rule
]
lt <<= 'Literal', [
    unescape[[str, p.Literal, str], p.Literal],
    unescape[[str, p.Literal, str], p.Literal],
]
lt <<= 'Text1', [
    text_accum_1,
    text_accum_2,
]
lt <<= 'Text2', [
    text_accum_1,
    text_accum_2,
]
lt <<= 'Character', [
    identity[[str], str]
] * 3
lt <<= 'Letter', [
    identity[[str], str]
] * 26 * 2
lt <<= 'Digit', [
    identity[[str], str]
] * 10
lt <<= 'Symbol', [
    identity[[str], str]
] * len(ALLOWED_SYMBOLS)
lt <<= 'Character1', [
    identity[[str], str],
    identity[[str], str]
]
lt <<= 'Character2', [
    identity[[str], str],
    identity[[str], str]
]
lt <<= 'RuleName', [
    identity[[str], str],
    add[[str, str], str]
]
lt <<= 'RuleEnd', [
    identity[[str], str],
    add[[str, str], str]
]
lt <<= 'OneRuleEnd', [
    identity[[str], str],
    identity[[str], str],
    add[[str, str], str],
    add[[str, str], str]
]
