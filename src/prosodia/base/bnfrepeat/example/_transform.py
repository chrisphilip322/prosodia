import typing

from ....core import grammar as g, transform as t
from ....validation.transform_validation import annotate

if typing.TYPE_CHECKING:
    T = typing.TypeVar('T')
    T2 = typing.TypeVar('T2')
    Addable = typing.TypeVar('Addable', str, list)


def syntax_accum(
    values: typing.Tuple[typing.Sequence[g.Rule], None]
) -> g.Language:
    rules = values[0]
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
        lang.add_rule(rule)
    return lang


def rule_accum(
    values: typing.Tuple[
        None,
        str,
        g.RuleName,
        str,
        None,
        str,
        None,
        typing.List[g.TermGroup],
        typing.Sequence[None]
    ]
) -> g.Rule:
    return g.Rule(values[2], g.Syntax(values[7]))


def expression_accum(
    values: typing.Tuple[
        g.TermGroup,
        typing.Sequence[g.TermGroup]
    ]
) -> typing.List[g.TermGroup]:
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


def base_term_accum_rule(
    values: typing.Tuple[str, g.RuleName, str]
) -> g.Term:
    return g.RuleReference(values[1])


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


def repeat_term_accum(
    values: typing.Tuple[
        g.Term,
        str,
        typing.Tuple[int, typing.Optional[int]],
        str
    ]
) -> g.Term:
    return g.RepeatTerm(values[0], values[2][0], values[2][1])


def repeat_body_accum1(
    values: typing.Tuple[str]
) -> typing.Tuple[int, typing.Optional[int]]:
    num = int(values[0])
    return (num, num)


def repeat_body_accum2(
    values: typing.Tuple[str, str]
) -> typing.Tuple[int, typing.Optional[int]]:
    num = int(values[0])
    return (num, None)


def repeat_body_accum3(
    values: typing.Tuple[str, str, str]
) -> typing.Tuple[int, typing.Optional[int]]:
    return (int(values[0]), int(values[2]))


def expression_end_accum(
    values: typing.Tuple[None, str, None, g.TermGroup]
) -> g.TermGroup:
    return values[3]


def list_end_accum(
    values: typing.Tuple[None, g.Term]
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


def list_of(
    values: typing.Tuple['T']
) -> typing.List['T']:
    return [values[0]]


def push_list(
    values: typing.Tuple['T', typing.List['T']]
) -> typing.List['T']:
    return [values[0]] + values[1]


def nothing(_: typing.Tuple['T']) -> None:
    return None


def nothing2(_: typing.Tuple['T', 'T2']) -> None:
    return None


def identity(values: typing.Tuple['T']) -> 'T':
    return values[0]


def identity2(values: typing.Tuple['T']) -> 'T2':
    return values[0]  # type: ignore


def unescape(
    values: typing.Tuple[str, 'T', str]
) -> 'T':
    return values[1]


def add(
    values: typing.Tuple['Addable', 'Addable']
) -> 'Addable':
    iterable = iter(values)
    accum = next(iterable)
    for item in iterable:
        accum += item
    return accum


def text_accum(
    values: typing.Tuple[typing.Sequence[str]]
) -> g.Literal:
    iterable = iter(values[0])
    accum = next(iterable)
    for item in iterable:
        accum += item
    return g.Literal(accum)


transform = t.LanguageTransformation.create('Syntax', [syntax_accum])
transform <<= 'Rule', [rule_accum]
transform <<= 'OptWhitespace', [
    annotate(nothing, T=typing.Sequence[str])
]
transform <<= 'Expression', [
    expression_accum
]
transform <<= 'SingleLineEnd', [
    annotate(nothing2, T=None, T2=None)
]
transform <<= 'List', [
    list_accum
]
transform <<= 'BaseTerm', [
    annotate(identity2, T=g.Literal, T2=g.Term),
    base_term_accum_rule,
    annotate(identity2, T=g.LiteralRange, T2=g.Term),
]
transform <<= 'Literal', [
    annotate(unescape, T=g.Literal),
    annotate(unescape, T=g.Literal),
]
transform <<= 'Text1', [
    text_accum
]
transform <<= 'Text2', [
    text_accum
]
transform <<= 'Character', [
    annotate(identity, T=str)
] * 3
transform <<= 'Letter', [
    annotate(identity, T=str)
] * 2
transform <<= 'Digit', [
    annotate(identity, T=str)
] * 2
transform <<= 'NonZeroDigit', [
    annotate(identity, T=str)
] * 1
transform <<= 'Symbol', [
    annotate(identity, T=str)
] * 6
transform <<= 'Character1', [
    annotate(identity, T=str),
    annotate(identity, T=str)
]
transform <<= 'Character2', [
    annotate(identity, T=str),
    annotate(identity, T=str)
]
transform <<= 'RuleName', [
    rule_name_accum
]
transform <<= 'OneRuleEnd', [
    annotate(identity, T=str),
    annotate(identity, T=str),
    annotate(add, Addable=str),
    annotate(add, Addable=str)
]
transform <<= 'EOL', [
    annotate(nothing, T=str)
]
transform <<= 'EOF', [
    annotate(nothing, T=str)
]
transform <<= 'LiteralRange', [
    literal_range_accum1,
    literal_range_accum2,
]
transform <<= 'Number', [
    annotate(identity, T=str),
    number_accum
]
transform <<= 'Term', [
    annotate(identity, T=g.Term),
    repeat_term_accum
]
transform <<= 'RepeatBody', [
    repeat_body_accum1,
    repeat_body_accum2,
    repeat_body_accum3,
]
transform <<= 'ExpressionEnd', [
    expression_end_accum
]
transform <<= 'ListEnd', [
    list_end_accum
]
