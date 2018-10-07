from prosodia.core.grammar import Grammar, Language

from ._text import text
from ._transform import transform
from ._intermediate_parser import create_intermediate_augmentedbnf
from ._freebies import add_freebie_rules


def create_language() -> Language:
    lang = create_intermediate_augmentedbnf().apply(text)
    add_freebie_rules(lang)
    return lang


def create_augmentedbnf() -> Grammar[Language]:
    return Grammar(create_language(), transform, False)
