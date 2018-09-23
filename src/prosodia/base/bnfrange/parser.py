from prosodia.core.grammar import Language
from ..bnf.parser import create_language as _create_base_language
from ..bnf.transform import lt as bnftransform
from .text import bnfrangetext

ALLOWED_SYMBOLS = r'| !#$%&()*+,-./:;>=<?@[\]^_`{}~'

def create_language() -> Language:
    return bnftransform.transform(_create_base_language().parse(bnfrangetext))
