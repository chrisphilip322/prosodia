import unittest

from prosodia.base.augmentedbnf.text import augmentedbnf_text
from prosodia.base.augmentedbnf.parser import create_language
from prosodia.base.augmentedbnf.transform import lt as transform
from prosodia.base.augmentedbnf.example import (
    example_augmentedbnf_text, example_transform)


class TestAugmentedBNF(unittest.TestCase):
    def _validate(self, validity):
        for msg in validity.messages:
            print(msg)
        self.assertTrue(validity)

    def test_augmentedbnf_parser_works(self):
        '''augmented_bnf is not a gramatical superset of bnf so we can't parse
        its bnf with itself
        '''
        # tree = lang.parse(augmentedbnf_text)
        # parsed_lang = transform.transform(tree)
        # self.assertTrue(parsed_lang.equals(lang))
        # tree2 = parsed_lang.parse(augmentedbnf_text)
        # parsed_lang2 = transform.transform(tree2)
        # self.assertTrue(parsed_lang2.equals(lang))
        # self.assertTrue(parsed_lang2.equals(parsed_lang))

        # self.assertTrue(lang.validate())
        # self.assertTrue(parsed_lang.validate())
        # self.assertTrue(parsed_lang2.validate())

        # self._validate(transform, lang)
        # self._validate(transform, parsed_lang)
        # self._validate(transform, parsed_lang2)

    def test_augmentedbnf_example_parser_works(self):
        lang = create_language()
        self._validate(lang.validate())
        self._validate(transform.validate(lang))
        # lang.debug = True
        tree = lang.parse(example_augmentedbnf_text)
        parsed_lang = transform.transform(tree)

        # self._validate(example_transform, parsed_lang)

        # example_tree = parsed_lang.parse(example_augmentedbnf_text)
        # example_parsed_lang = example_transform.transform(example_tree)

        # example_tree2 = example_parsed_lang.parse(example_augmentedbnf_text)
        # example_parsed_lang2 = example_transform.transform(example_tree2)

        # self.assertTrue(example_parsed_lang2.equals(example_parsed_lang))

        # self.assertTrue(example_parsed_lang.validate())
        # self.assertTrue(example_parsed_lang2.validate())

        # self._validate(example_transform, example_parsed_lang)
        # self._validate(example_transform, example_parsed_lang2)


if __name__ == '__main__':
    TestAugmentedBNF.test_augmentedbnf_example_parser_works(None)
