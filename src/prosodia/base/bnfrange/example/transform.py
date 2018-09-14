import typing

from ....core import grammar as g, transform as t
from ....validation.new_transform_validation import annotate

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


lt = t.LanguageTransformation.create()
lt <<= 'Syntax', [syntax_accum]
lt <<= 'Rules', [
    annotate(list_of, T=g.Rule),
    annotate(push_list, T=g.Rule)
]
lt <<= 'Rule', [rule_accum]
lt <<= 'OptWhitespace', [
    annotate(nothing2, T=str, T2=None),
    annotate(nothing, T=str)
]
lt <<= 'Expression', [
    annotate(list_of, T=g.TermGroup),
    expression_accum
]
lt <<= 'LineEnd', [
    annotate(nothing, T=None),
    annotate(nothing2, T=None, T2=None),
]
lt <<= 'SingleLineEnd', [
    annotate(nothing2, T=None, T2=None)
]
lt <<= 'List', [
    list_accum_1,
    list_accum_2
]
lt <<= 'Term', [
    annotate(identity2, T=g.Literal, T2=g.Term),
    term_accum_rule,
    annotate(identity2, T=g.LiteralRange, T2=g.Term),
]
lt <<= 'Literal', [
    annotate(unescape, T=g.Literal),
    annotate(unescape, T=g.Literal),
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
lt <<= 'Character1', [
    annotate(identity, T=str),
    annotate(identity, T=str)
]
lt <<= 'Character2', [
    annotate(identity, T=str),
    annotate(identity, T=str)
]
lt <<= 'RuleName', [
    annotate(identity, T=str),
    annotate(add, Addable=str)
]
lt <<= 'RuleEnd', [
    annotate(identity, T=str),
    annotate(add, Addable=str)
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
lt <<= 'LiteralRange', [
    literal_range_accum1,
    literal_range_accum2,
]
lt <<= 'Number', [
    annotate(identity, T=str),
    annotate(add, Addable=str)
]
lt <<= 'Digits', [
    annotate(identity, T=str),
    annotate(add, Addable=str)
]
