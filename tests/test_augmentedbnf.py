import unittest

from prosodia.base.augmentedbnf import create_augmentedbnf
from prosodia.base.augmentedbnf._text import text
from prosodia.base.augmentedbnf._parser import create_intermediate_augmentedbnf

from _helpers import validate_recursive_grammar, validate


class TestAugmentedBNF(unittest.TestCase):
    def test_augmentedbnf_example_parser_works(self):
        validate_recursive_grammar(self, create_augmentedbnf(), text)

    def test_intermediate_augmented_bnf(self):
        inter_abnf = create_intermediate_augmentedbnf()
        validate(self, inter_abnf.validate())

        parsed_lang = inter_abnf.apply(text)
        validate(self, parsed_lang.validate())
