from prosodia.core.grammar import Grammar, Language

from ._parser import create_language
from ._transform import transform


def create_bnfrange() -> Grammar[Language]:
    return Grammar(create_language(), transform)
