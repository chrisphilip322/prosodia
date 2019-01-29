import unittest

from prosodia.base.augmentedbnf import create_augmentedbnf
from prosodia.base.augmentedbnf._text import text
from prosodia.base.augmentedbnf._intermediate_parser import (
    create_intermediate_augmentedbnf
)
from prosodia.base.augmentedbnf._freebies import add_freebie_rules

from ._helpers import validate_recursive_grammar, validate


class TestAugmentedBNF(unittest.TestCase):
    def test_augmentedbnf_parser_works(self) -> None:
        abnf = create_augmentedbnf()
        validate_recursive_grammar(self, abnf, text)

    def test_intermediate_augmented_bnf(self) -> None:
        inter_abnf = create_intermediate_augmentedbnf()
        validate(self, inter_abnf.validate())

        parsed_lang = inter_abnf.apply(text)
        add_freebie_rules(parsed_lang)
        validate(self, parsed_lang.validate())
