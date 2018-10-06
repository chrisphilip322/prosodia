import unittest


from prosodia.base.augmentedbnf import create_augmentedbnf
from prosodia.base.augmentedbnf._text import text

from _helpers import validate_recursive_grammar


class TestAugmentedBNF(unittest.TestCase):
    def test_augmentedbnf_example_parser_works(self):
        validate_recursive_grammar(self, create_augmentedbnf(), text)

    def test_intermediate_augmented_bnf(self):
        pass
