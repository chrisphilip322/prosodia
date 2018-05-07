from unittest import TestCase

from prosodia.base.abnf.text import abnf

from prosodia.base.bnf.text import bnf
from prosodia.base.bnf.parser import lang as bnf_lang
from prosodia.base.bnf.transform import lt as bnf_transform


class TestABNF(TestCase):
    def test_abnf_parser_works(self):
        tree = bnf_lang.parse(abnf)
        abnf_lang = bnf_transform.transform(tree)
        self.assertTrue(abnf_lang)
