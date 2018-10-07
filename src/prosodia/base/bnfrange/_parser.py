from prosodia.core.grammar import Language

from ..bnf import create_bnf
from ._text import text


def create_language() -> Language:
    return create_bnf().apply(text)
