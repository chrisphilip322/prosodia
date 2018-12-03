from typing import Sequence, Tuple

from prosodia.core.grammar import Language
from prosodia.core.transform import LanguageTransformation
from prosodia.validation.transform_validation import annotate
from prosodia.validation.group_types import Group2, NoValue

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
        Group2[
            Tuple[str],
            Tuple[str, str]
        ]
    ]]
) -> str:
    total = ''
    for i in values[0]:
        cand1, cand2 = i
        if not isinstance(cand1, NoValue):
            total += cand1[0]
        elif not isinstance(cand2, NoValue):
            total += cand2[0] + cand2[1]
    return total
