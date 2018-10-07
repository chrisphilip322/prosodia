from prosodia.core.grammar import Grammar, Language

from ..bnfrepeat import create_bnfrepeat

from ._intermediate_text import intermediate_text
from ._intermediate_transform import intermediate_transform


def create_intermediate_language() -> Language:
    return create_bnfrepeat().apply(intermediate_text)


def create_intermediate_augmentedbnf() -> Grammar[Language]:
    return Grammar(create_intermediate_language(), intermediate_transform)
