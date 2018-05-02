import mypy.main
from unittest import TestCase


class TestTyping(TestCase):
    def test_typing(self):
        mypy.main.main(None, ['src/', '--strict'])
