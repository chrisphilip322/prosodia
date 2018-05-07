import mypy.main
from unittest import TestCase, skip


class TestTyping(TestCase):
    def test_typing(self):
        # TODO: make this --strict?
        mypy.main.main(
            None,
            [
                'src/',
                '--disallow-untyped-defs',
                '--disallow-incomplete-defs'
            ]
        )
