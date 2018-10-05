import unittest

from prosodia.core.grammar import Grammar
from prosodia.base.bnfrange import create_bnfrange
from prosodia.base.bnfrange._text import text
from prosodia.base.bnfrange.example import create_example_bnfrange
from prosodia.base.bnfrange.example._text import example_text


class TestBNFRange(unittest.TestCase):
    def _validate(self, validity):
        for msg in validity.messages:
            print(msg)
        self.assertTrue(validity)

    def test_bnf_range_parser_works(self):
        bnfrange = create_bnfrange()
        self._validate(bnfrange.validate())

        parsed_lang = bnfrange.apply(text)
        parsed_grammar = Grammar(parsed_lang, bnfrange.transform)
        self.assertTrue(parsed_lang.equals(bnfrange.language))
        self._validate(parsed_grammar.validate())

        parsed_lang2 = parsed_grammar.apply(text)
        parsed_grammar2 = Grammar(parsed_lang2, bnfrange.transform)
        self.assertTrue(parsed_lang2.equals(bnfrange.language))
        self.assertTrue(parsed_lang2.equals(parsed_lang))
        self._validate(parsed_grammar2.validate())

    def test_bnf_range_example_parser_works(self):
        example_bnfrange = create_example_bnfrange()
        self._validate(example_bnfrange.validate())

        parsed_lang = example_bnfrange.apply(example_text)
        parsed_grammar = Grammar(parsed_lang, example_bnfrange.transform)
        self.assertTrue(example_bnfrange.language.equals(parsed_lang))
        self._validate(parsed_grammar.validate())

        parsed_lang2 = parsed_grammar.apply(example_text)
        parsed_grammar2 = Grammar(parsed_lang2, example_bnfrange.transform)
        self.assertTrue(example_bnfrange.language.equals(parsed_lang2))
        self.assertTrue(parsed_lang.equals(parsed_lang2))
        self._validate(parsed_grammar2.validate())
