import unittest

from prosodia.base.bnf.text import bnf
from prosodia.base.bnf.parser import lang
from prosodia.base.bnf.transform import lt as transform

class TestBNF(unittest.TestCase):
    def test_bnf_parser_works(self):
        tree = lang.parse(bnf)
        parsed_lang = transform.transform(tree)
        self.assertEqual(parsed_lang, lang)
        tree2 = parsed_lang.parse(bnf)
        parsed_lang2 = transform.transform(tree2)
        self.assertEqual(parsed_lang2, lang)
        self.assertEqual(parsed_lang2, parsed_lang)

        self.assertTrue(lang.validate())
        self.assertTrue(parsed_lang.validate())
        self.assertTrue(parsed_lang2.validate())

        self.assertTrue(transform.validate(lang))
        self.assertTrue(transform.validate(parsed_lang))
        self.assertTrue(transform.validate(parsed_lang2))
