import unittest

from prosodia.base.bnfrepeat.text import bnfrepeattext
from prosodia.base.bnfrepeat.parser import lang
from prosodia.base.bnfrepeat.transform import lt as transform
from prosodia.base.bnfrepeat.example import (
    example_bnfrepeattext, example_transform)

class TestBNFRange(unittest.TestCase):
    def _validate(self, t, l):
        validity = t.validate(l)
        for msg in validity.messages:
            print(msg)
        self.assertTrue(validity)

    def test_bnf_range_parser_works(self):
        tree = lang.parse(bnfrepeattext)
        parsed_lang = transform.transform(tree)
        self.assertTrue(parsed_lang.equals(lang))
        tree2 = parsed_lang.parse(bnfrepeattext)
        parsed_lang2 = transform.transform(tree2)
        self.assertTrue(parsed_lang2.equals(lang))
        self.assertTrue(parsed_lang2.equals(parsed_lang))

        self.assertTrue(lang.validate())
        self.assertTrue(parsed_lang.validate())
        self.assertTrue(parsed_lang2.validate())

        self._validate(transform, lang)
        self._validate(transform, parsed_lang)
        self._validate(transform, parsed_lang2)

    def test_bnf_range_example_parser_works(self):
        tree = lang.parse(example_bnfrepeattext)
        parsed_lang = transform.transform(tree)

        self._validate(example_transform, parsed_lang)

        example_tree = parsed_lang.parse(example_bnfrepeattext)
        example_parsed_lang = example_transform.transform(example_tree)

        example_tree2 = example_parsed_lang.parse(example_bnfrepeattext)
        example_parsed_lang2 = example_transform.transform(example_tree2)

        self.assertTrue(example_parsed_lang2.equals(example_parsed_lang))

        self.assertTrue(example_parsed_lang.validate())
        self.assertTrue(example_parsed_lang2.validate())

        self._validate(example_transform, example_parsed_lang)
        self._validate(example_transform, example_parsed_lang2)
