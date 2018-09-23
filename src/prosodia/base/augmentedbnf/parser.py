from prosodia.core.grammar import Language
from ..bnfrepeat.parser import create_language as _base_create_language
from ..bnfrepeat.transform import lt as _base_transform
from .text import augmentedbnf_text


def create_language() -> Language:
    return _base_transform.transform(
        _base_create_language().parse(augmentedbnf_text)
    )
