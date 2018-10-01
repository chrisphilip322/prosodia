import unittest

from prosodia.base.augmentedbnf.text import augmentedbnf_text
from prosodia.base.augmentedbnf.parser import create_language
from prosodia.base.augmentedbnf.transform import lt as transform
from prosodia.base.augmentedbnf.example import (
    example_augmentedbnf_text,
    example_group_augmentedbnf_text,
    group_transform
)


class TestAugmentedBNF(unittest.TestCase):
    def _validate(self, validity):
        for msg in validity.messages:
            print(msg)
        self.assertTrue(validity)

    def test_augmentedbnf_example_parser_works(self):
        lang = create_language()
        self._validate(lang.validate())
        self._validate(transform.validate(lang))
        tree = lang.parse(example_augmentedbnf_text)
        parsed_lang = transform.transform(tree)
        self._validate(parsed_lang.validate())
        self._validate(transform.validate(parsed_lang))

        prime_tree = parsed_lang.parse(example_augmentedbnf_text)
        prime_lang = transform.transform(prime_tree)
        self._validate(prime_lang.validate())
        self._validate(transform.validate(prime_lang))

        self._validate(lang.equals(parsed_lang))
        self._validate(lang.equals(prime_lang))

    def test_augmentedbnf_group_terms_work(self):
        lang = create_language()
        tree = lang.parse(example_group_augmentedbnf_text)
        parsed_lang = transform.transform(tree)

        group_tree = parsed_lang.parse(example_group_augmentedbnf_text)
        group_lang = group_transform.transform(group_tree)
        self._validate(group_lang.validate())
        self._validate(group_transform.validate(group_lang))
        self._validate(parsed_lang.equals(group_lang))
