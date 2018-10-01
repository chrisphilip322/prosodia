import typing

from ....core import grammar as g, transform as t
from ....validation.transform_validation import annotate

from .._transform_helpers import (
    nothing, nothing2, nothing3, identity, identity2, add, unescape)
from .._transform_terminals import add_terminal_transforms


def rule_reference_accum(values: typing.Tuple[str]) -> g.Term:
    return g.RuleReference(values[0])


def syntax_accum(
    values: typing.Tuple[
        typing.Sequence[
            typing.Union[g.Rule, typing.Tuple[str, typing.List[g.TermGroup]]]
        ],
        None
    ]
) -> g.Language:
    rules = values[0]
    if not isinstance(rules[0], g.Rule):
        raise TypeError('First rule cannot use "=/"')
    lang = g.Language.create(rules[0].name)
    eol_rule = g.Rule(
        'EOL',
        g.Syntax.create(
            g.TermGroup.create(
                g.Literal('\n')
            )
        )
    )
    eof_rule = g.Rule(
        'EOF',
        g.Syntax.create(
            g.TermGroup.create(
                g.EOFTerm()
            )
        )
    )
    lang.add_rule(eol_rule)
    lang.add_rule(eof_rule)
    for rule in rules:
        if isinstance(rule, g.Rule):
            lang.add_rule(rule)
        else:
            lang.add_to_rule(rule[0], rule[1])
    return lang


def rule_accum(
    values: typing.Tuple[
        None,
        str,
        None,
        str,
        None,
        typing.List[g.TermGroup],
        typing.Sequence[None]
    ]
) -> typing.Union[g.Rule, typing.Tuple[str, typing.List[g.TermGroup]]]:
    if values[3] == '=':
        return g.Rule(values[1], g.Syntax(values[5]))
    elif values[3] == '=/':
        return values[1], values[5]
    else:
        raise RuntimeError


def expression_accum(
    values: typing.Tuple[
        g.TermGroup,
        typing.Sequence[g.TermGroup]
    ]
) -> typing.List[g.TermGroup]:
    # TO DO: return a list of lists instead
    return [values[0]] + list(values[1])


def list_accum(
    values: typing.Tuple[g.Term, typing.Sequence[g.Term]]
) -> g.TermGroup:
    return g.TermGroup([values[0]] + list(values[1]))


def text_accum_1(
    values: typing.Tuple[str]
) -> g.Literal:
    return g.Literal(values[0])


def text_accum_2(
    values: typing.Tuple[str, g.Literal]
) -> g.Literal:
    return g.Literal(values[0] + values[1].text)


def literal_range_accum1(
    values: typing.Tuple[str, str, str]
) -> g.LiteralRange:
    number = int(values[1])
    return g.LiteralRange(number, number)


def literal_range_accum2(
    values: typing.Tuple[str, str, str, str, str]
) -> g.LiteralRange:
    first = int(values[1])
    second = int(values[3])
    return g.LiteralRange(first, second)


def repeat_body_accum1(
    values: typing.Tuple[typing.Sequence[str], str, typing.Sequence[str]]
) -> typing.Tuple[int, typing.Optional[int]]:
    if values[0]:
        start = int(values[0][0])
    else:
        start = 0
    if values[2]:
        end: typing.Optional[int] = int(values[2][0])
    else:
        end = None
    return (start, end)


def repeat_body_accum2(
    values: typing.Tuple[str]
) -> typing.Tuple[int, typing.Optional[int]]:
    num = int(values[0])
    return (num, num)


def expression_end_accum(
    values: typing.Tuple[None, str, None, g.TermGroup]
) -> g.TermGroup:
    return values[3]


def list_end_accum(
    values: typing.Tuple[typing.Sequence[str], g.Term]
) -> g.Term:
    return values[1]


def number_accum(
    values: typing.Tuple[str, typing.Sequence[str]]
) -> str:
    val = values[0]
    for x in values[1]:
        val += x
    return val


def rule_name_accum(
    values: typing.Tuple[str, typing.Sequence[str]]
) -> str:
    val = values[0]
    for x in values[1]:
        val += x
    return val


def text_accum(
    values: typing.Tuple[typing.Sequence[str]]
) -> g.Literal:
    iterable = iter(values[0])
    accum = next(iterable)
    for item in iterable:
        accum += item
    return g.Literal(accum)


def _repeat_term_accum1(
    values: typing.Tuple[typing.Tuple[int, typing.Optional[int]], g.Term]
) -> g.Term:
    ((start, end), term) = values
    return g.RepeatTerm(term, start, end)


def _repeat_term_accum2(
    values: typing.Tuple[str, g.Term, str]
) -> g.Term:
    return g.RepeatTerm(values[1], 0, 1)


def _string_literal_accum(
    values: typing.Tuple[
        typing.Sequence[
            typing.Tuple[
                int,
                typing.Union[
                    typing.Tuple[str],
                    typing.Tuple[str]
                ]
            ]
        ],
        typing.Sequence[str]
    ]
) -> g.Literal:
    value = ''.join(values[1])
    if values[0]:
        sensitivity = values[0][1][0]
        if sensitivity == "%s":
            return g.Literal(value, True)
        elif sensitivity == "%i":
            return g.Literal(value, False)
        else:
            raise RuntimeError('unreachable')
    else:
        return g.Literal(value, False)


def _string_literal_accum2(
    values: typing.Tuple[str, typing.Sequence[str]]
) -> g.Literal:
    (sensitivity, list_value) = values
    value = ''.join(list_value)
    if sensitivity == "%s":
        return g.Literal(value, True)
    elif sensitivity == "%i":
        return g.Literal(value, False)
    else:
        raise RuntimeError('unreachable')


def _group_term_accum(
    values: typing.Tuple[str, None, typing.List[g.TermGroup], None, str]
) -> g.Term:
    return g.GroupTerm([
        term_group.terms
        for term_group in values[2]
    ])


lt = t.LanguageTransformation.create()
lt <<= 'Syntax', [syntax_accum]
lt <<= 'Rule', [rule_accum]
lt <<= 'OptWhitespace', [
    annotate(nothing, T=typing.Sequence[str])
]
lt <<= 'Expression', [
    expression_accum
]
lt <<= 'SingleLineEnd', [
    annotate(nothing3, T=None, T2=typing.Sequence[None], T3=None)
]
lt <<= 'List', [
    list_accum
]
lt <<= 'RepeatableTerm', [
    annotate(identity2, T=g.Literal, T2=g.Term),
    annotate(identity, T=g.Term),
    annotate(identity, T=g.Term),
    annotate(identity, T=g.Term),
    rule_reference_accum,
    annotate(identity, T=g.Term),
]
lt <<= 'LiteralBody', [
    annotate(unescape, T=typing.Sequence[str])
]
lt <<= 'Character', [
    annotate(identity, T=str)
] * 3
lt <<= 'Letter', [
    annotate(identity, T=str)
] * 2
lt <<= 'Digit', [
    annotate(identity, T=str)
] * 2
lt <<= 'NonZeroDigit', [
    annotate(identity, T=str)
] * 1
lt <<= 'Symbol', [
    annotate(identity, T=str)
] * 6
lt <<= 'RuleName', [
    rule_name_accum
]
lt <<= 'OneRuleEnd', [
    annotate(identity, T=str),
    annotate(identity, T=str),
    annotate(add, Addable=str),
    annotate(add, Addable=str)
]
lt <<= 'EOL', [
    annotate(nothing, T=str)
]
lt <<= 'EOF', [
    annotate(nothing, T=str)
]
lt <<= 'Number', [
    annotate(identity, T=str),
    number_accum
]
lt <<= 'Term', [
    annotate(identity, T=g.Term),
    annotate(identity, T=g.Term),
]
lt <<= 'RepeatBody', [
    repeat_body_accum1,
    repeat_body_accum2,
]
lt <<= 'ExpressionEnd', [
    expression_end_accum
]
lt <<= 'ListEnd', [
    list_end_accum
]
lt <<= 'RepeatTerm', [
    _repeat_term_accum1,
    _repeat_term_accum2
]
lt <<= 'AssignmentOperator', [annotate(identity, T=str)] * 2
lt <<= 'Comment', [annotate(nothing2, T=str, T2=typing.Sequence[str])]
lt <<= 'StringLiteral', [
    _string_literal_accum,
]
lt <<= 'GroupTerm', [_group_term_accum]
lt = add_terminal_transforms(lt)


__all__ = ['lt']
