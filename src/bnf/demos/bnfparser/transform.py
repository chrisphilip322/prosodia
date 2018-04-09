import typing

from ...core import grammar as g, transform as t
from ...validation.transform_validation import TypeAdder
from .parser import ALLOWED_SYMBOLS

S = typing.TypeVar('S')
T = typing.TypeVar('T')
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
        typing.List[g.TermGroup]
    ]
) -> typing.List[g.TermGroup]:
    return [values[0]] + values[4]

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
    values: typing.Tuple[Addable, ...]
) -> Addable:
    iterable = iter(values)
    accum = next(iterable)
    for item in iterable:
        accum += item
    return accum


lt = t.LanguageTransformation.create()
lt <<= 'Syntax', [syntax_accum]
lt <<= 'Rules', [
    list_of[[g.Rule], typing.Sequence[g.Rule]],
    push_list[[g.Rule, typing.Sequence[g.Rule]], typing.Sequence[g.Rule]]
]
lt <<= 'Rule', [rule_accum]
lt <<= 'OptWhitespace', [
    nothing[[str, None], None],
    nothing[[str], None]
]
lt <<= 'Expression', [
    list_of[[g.TermGroup], typing.List[g.TermGroup]],
    expression_accum
]
lt <<= 'LineEnd', [
    nothing[[None], None],
    nothing[[None, None], None],
]
lt <<= 'SingleLineEnd', [
    nothing[[None, None], None]
]
lt <<= 'List', [
    list_accum_1,
    list_accum_2
]
lt <<= 'Term', [
    identity[[g.Literal], g.Term],
    term_accum_rule
]
lt <<= 'Literal', [
    unescape[[str, g.Literal, str], g.Literal],
    unescape[[str, g.Literal, str], g.Literal],
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
lt <<= 'EOL', [
    nothing[[str], None]
]
lt <<= 'EOF', [
    nothing[[str], None]
]
