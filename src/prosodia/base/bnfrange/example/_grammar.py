from prosodia.core.grammar import Grammar, Language

from .. import create_bnfrange
from ._text import example_text
from ._transform import transform


def create_example_bnfrange() -> Grammar[Language]:
    return Grammar(
        create_bnfrange().apply(example_text),
        transform
    )
