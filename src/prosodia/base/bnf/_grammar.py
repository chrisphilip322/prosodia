from prosodia.core.grammar import Grammar, Language

from ._parser import create_language
from ._transform import transform


def create_bnf() -> Grammar[Language]:
    return Grammar(create_language(), transform)
