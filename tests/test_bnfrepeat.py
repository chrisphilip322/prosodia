import unittest

from prosodia.base.bnfrepeat import create_bnfrepeat
from prosodia.base.bnfrepeat._text import text
from prosodia.base.bnfrepeat.example import create_example_bnfrepeat
from prosodia.base.bnfrepeat.example._text import example_text

from ._helpers import validate_recursive_grammar


class TestBNFRepeat(unittest.TestCase):
    def test_bnf_range_parser_works(self):
        validate_recursive_grammar(self, create_bnfrepeat(), text)

    def test_bnf_range_example_parser_works(self):
        validate_recursive_grammar(
            self,
            create_example_bnfrepeat(),
            example_text
        )
