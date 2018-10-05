import traceback
from unittest import TestCase, mock

from prosodia.core.grammar import Grammar
from prosodia.base.bnf import create_bnf
from prosodia.base.bnf._text import text
from prosodia.core.transform import TermGroupTransformation


def fake_tgt(stacks):
    real_transform = TermGroupTransformation.transform

    def wrapped(*args, **kwargs):
        stacks.append(traceback.extract_stack())
        return real_transform(*args, **kwargs)
    return wrapped


class TestBNF(TestCase):
    def _assert_validity(self, validity):
        for msg in validity.messages:
            print(msg)
        self.assertTrue(validity)

    def test_bnf_parser_works(self):
        bnf = create_bnf()
        self._assert_validity(bnf.validate())

        parsed_lang = bnf.apply(text)
        parsed_grammar = Grammar(parsed_lang, bnf.transform)
        self.assertTrue(parsed_lang.equals(bnf.language))
        self._assert_validity(parsed_grammar.validate())

        parsed_lang2 = parsed_grammar.apply(text)
        parsed_grammar2 = Grammar(parsed_lang2, bnf.transform)
        self.assertTrue(parsed_lang2.equals(bnf.language))
        self.assertTrue(parsed_lang2.equals(parsed_lang))
        self._assert_validity(parsed_grammar2.validate())

    def test_no_arbitrary_recursion(self):
        bnf = create_bnf()
        stack = traceback.extract_stack()
        stacks = []
        with mock.patch(
            'prosodia.base.bnf._transform.t.TermGroupTransformation.transform',
            new=fake_tgt(stacks)
        ):
            parsed_lang = bnf.apply(text)
            parsed_grammar = Grammar(parsed_lang, bnf.transform)
            parsed_lang2 = parsed_grammar.apply(text)

            self._assert_validity(parsed_lang.equals(bnf.language))
            self.assertTrue(parsed_lang2.equals(bnf.language))
            self.assertTrue(parsed_lang2.equals(parsed_lang))

        largest = max(stacks, key=len)
        # 5 is kind of an arbitrary number and the minimum that makes this test
        # pass, it should just be low
        self.assertTrue(len(largest) <= len(stack) + 5)
