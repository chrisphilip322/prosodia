from prosodia.core.grammar import Grammar, Language

from ._parser import create_language
from ._transform import transform


def create_bnfrepeat() -> Grammar[Language]:
    return Grammar(create_language(), transform)
