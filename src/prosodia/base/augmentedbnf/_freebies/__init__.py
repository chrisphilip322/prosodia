from typing import Sequence, Tuple, Union

from prosodia.core.grammar import Grammar, Language
from prosodia.core.transform import LanguageTransformation
from prosodia.validation.transform_validation import annotate

from .._transform_helpers import add, identity

from .._intermediate_parser import create_intermediate_augmentedbnf
from .text import freebies_text


def add_freebie_rules(lang: Language) -> Language:
    abnf = create_intermediate_augmentedbnf()
    freebies = abnf.apply(freebies_text).rules
    for rule in freebies.values():
        lang.add_rule(rule)
    return lang


def add_freebie_transforms(
    lt: LanguageTransformation
) -> LanguageTransformation:
    lt <<= 'CR', [annotate(identity, T=str)]
    lt <<= 'CRLF', [annotate(add, Addable=str)]
    lt <<= 'CTL', [annotate(identity, T=str)] * 2
    lt <<= 'DIGIT', [annotate(identity, T=str)]
    lt <<= 'DQUOTE', [annotate(identity, T=str)]
    lt <<= 'HEXDIG', [annotate(identity, T=str)] * 7
    lt <<= 'HTAB', [annotate(identity, T=str)]
    lt <<= 'LF', [annotate(identity, T=str)]
    lt <<= 'LWSP', [lwsp_accum]
    lt <<= 'OCTET', [annotate(identity, T=str)]
    lt <<= 'SP', [annotate(identity, T=str)]
    lt <<= 'VCHAR', [annotate(identity, T=str)]
    lt <<= 'WSP', [annotate(identity, T=str)] * 2
    return lt


def lwsp_accum(
    values: Tuple[Sequence[
        Tuple[
            int,
            Union[
                Tuple[str],
                Tuple[str, str]
            ]
        ]
    ]]
) -> str:
    return sum(
        (
            sum(item[1], '')
            for item in values[0]
        ),
        ''
    )
