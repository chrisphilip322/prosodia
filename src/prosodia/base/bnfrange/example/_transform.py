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
        typing.Sequence[g.TermGroup],
        None
    ]
) -> g.Rule:
    return g.Rule(values[2], g.Syntax(values[7]))


def expression_accum(
    values: typing.Tuple[
        g.TermGroup,
        None,
        str,
        None,
        typing.Sequence[g.TermGroup]
    ]
) -> typing.Sequence[g.TermGroup]:
    return [values[0]] + list(values[4])


def list_accum_1(
    values: typing.Tuple[g.Term]
) -> g.TermGroup:
    return g.TermGroup(list(values))


def list_accum_2(
    values: typing.Tuple[g.Term, None, g.TermGroup]
) -> g.TermGroup:
    return g.TermGroup([values[0]] + list(values[2].terms))


def text_accum_1(
    values: typing.Tuple[str]
) -> g.Literal:
    return g.Literal(values[0])


def text_accum_2(
    values: typing.Tuple[str, g.Literal]
) -> g.Literal:
    return g.Literal(values[0] + values[1].text)


def term_accum_rule(
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


def list_of(
    values: typing.Tuple['T']
) -> typing.Sequence['T']:
    return [values[0]]


def push_list(
    values: typing.Tuple['T', typing.Sequence['T']]
) -> typing.Sequence['T']:
    return [values[0]] + list(values[1])


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


transform = t.LanguageTransformation.create('Syntax', [syntax_accum])
transform <<= 'Rules', [
    annotate(list_of, T=g.Rule),
    annotate(push_list, T=g.Rule)
]
transform <<= 'Rule', [rule_accum]
transform <<= 'OptWhitespace', [
    annotate(nothing2, T=str, T2=None),
    annotate(nothing, T=str)
]
transform <<= 'Expression', [
    annotate(list_of, T=g.TermGroup),
    expression_accum
]
transform <<= 'LineEnd', [
    annotate(nothing, T=None),
    annotate(nothing2, T=None, T2=None),
]
transform <<= 'SingleLineEnd', [
    annotate(nothing2, T=None, T2=None)
]
transform <<= 'List', [
    list_accum_1,
    list_accum_2
]
transform <<= 'Term', [
    annotate(identity2, T=g.Literal, T2=g.Term),
    term_accum_rule,
    annotate(identity2, T=g.LiteralRange, T2=g.Term),
]
transform <<= 'Literal', [
    annotate(unescape, T=g.Literal),
    annotate(unescape, T=g.Literal),
]
transform <<= 'Text1', [
    text_accum_1,
    text_accum_2,
]
transform <<= 'Text2', [
    text_accum_1,
    text_accum_2,
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
    annotate(identity, T=str),
    annotate(add, Addable=str)
]
transform <<= 'RuleEnd', [
    annotate(identity, T=str),
    annotate(add, Addable=str)
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
    annotate(add, Addable=str)
]
transform <<= 'Digits', [
    annotate(identity, T=str),
    annotate(add, Addable=str)
]
