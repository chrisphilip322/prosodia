from prosodia.core.grammar import Grammar, Language

from .. import create_bnfrepeat
from ._text import example_text
from ._transform import transform


def create_example_bnfrepeat() -> Grammar[Language]:
    return Grammar(create_bnfrepeat().apply(example_text), transform)
