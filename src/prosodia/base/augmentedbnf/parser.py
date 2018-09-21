from ..bnfrepeat.parser import lang as _base_lang
from ..bnfrepeat.transform import lt as _base_transform
from .text import augmentedbnf_text

lang = _base_transform.transform(_base_lang.parse(augmentedbnf_text))
