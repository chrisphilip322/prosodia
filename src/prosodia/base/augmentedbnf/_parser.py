from prosodia.core.grammar import Language
from ..bnfrepeat import create_bnfrepeat
from ._text import text
from ._intermediate_text import intermediate_text
from ._transform import transform


def create_intermediate_language() -> Language:
    return create_bnfrepeat().apply(intermediate_text)


def create_language() -> Language:
    return transform.transform(create_intermediate_language().parse(text))
