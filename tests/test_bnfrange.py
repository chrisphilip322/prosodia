import unittest

from prosodia.base.bnfrange import create_bnfrange
from prosodia.base.bnfrange._text import text
from prosodia.base.bnfrange.example import create_example_bnfrange
from prosodia.base.bnfrange.example._text import example_text

from _helpers import validate_recursive_grammar


class TestBNFRange(unittest.TestCase):
    def test_bnf_range_parser_works(self):
        validate_recursive_grammar(self, create_bnfrange(), text)

    def test_bnf_range_example_parser_works(self):
        validate_recursive_grammar(
            self,
            create_example_bnfrange(),
            example_text
        )
