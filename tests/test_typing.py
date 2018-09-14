import mypy.main
from unittest import TestCase


class TestTyping(TestCase):
    def test_typing(self):
        # TODO: make this --strict?
        mypy.main.main(None, ['src/'])
