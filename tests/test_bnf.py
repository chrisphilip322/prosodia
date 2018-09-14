import traceback
import unittest

from prosodia.base.bnf.text import bnf
from prosodia.base.bnf.parser import lang
from prosodia.base.bnf.transform import lt as transform
from prosodia.core.transform import TermGroupTransformation


def fake_tgt(stacks):
    real_transform = TermGroupTransformation.transform
    def wrapped(*args, **kwargs):
        stacks.append(len(traceback.extract_stack()))
        return real_transform(*args, **kwargs)
    return wrapped


class TestBNF(unittest.TestCase):
    def _assert_validity(self, validity):
        for msg in validity.messages:
            print(msg)
        self.assertTrue(validity)

    def test_bnf_parser_works(self):
        tree = lang.parse(bnf)
        parsed_lang = transform.transform(tree)
        self.assertTrue(parsed_lang.equals(lang))
        tree2 = parsed_lang.parse(bnf)
        parsed_lang2 = transform.transform(tree2)
        self.assertTrue(parsed_lang2.equals(lang))
        self.assertTrue(parsed_lang2.equals(parsed_lang))

        self._assert_validity(lang.validate())
        self._assert_validity(parsed_lang.validate())
        self._assert_validity(parsed_lang2.validate())

        self._assert_validity(transform.validate(lang))
        self._assert_validity(transform.validate(parsed_lang))
        self._assert_validity(transform.validate(parsed_lang2))

    def test_no_arbitrary_recursion(self):
        stack = traceback.extract_stack()
        stacks = []
        with unittest.mock.patch(
            'prosodia.base.bnf.transform.t.TermGroupTransformation.transform',
            new=fake_tgt(stacks)
        ):
            tree = lang.parse(bnf)
            parsed_lang = transform.transform(tree)
            self._assert_validity(parsed_lang.equals(lang))
            tree2 = parsed_lang.parse(bnf)
            parsed_lang2 = transform.transform(tree2)
            self._assert_validity(parsed_lang2.equals(lang))
            self._assert_validity(parsed_lang2.equals(parsed_lang))
        self.assertTrue(max(stacks) < len(stack) + 5)
