import unittest
from unittest import mock

from prosodia.core.transform import LazySequenceTransform

class TestLazySequenceTransform(unittest.TestCase):
    def test_lazy_get(self):
        m = mock.Mock()
        mock_lang = mock.Mock()
        lst = LazySequenceTransform.create(
            [m.a, m.b, m.c],
            mock_lang
        )
        self.assertEqual(m.mock_calls, [])

        self.assertEqual(lst[0], m.a.transform.return_value)
        self.assertEqual(
            m.mock_calls,
            [mock.call.a.transform(mock_lang)]
        )

        # test repeat gets dont cause extra transform calls
        self.assertEqual(lst[0], m.a.transform.return_value)
        self.assertEqual(
            m.mock_calls,
            [mock.call.a.transform(mock_lang)]
        )

    def test_lazy_iter(self):
        m = mock.Mock()
        mock_lang = mock.Mock()
        lst = LazySequenceTransform.create(
            [m.a, m.b, m.c],
            mock_lang
        )
        self.assertEqual(m.mock_calls, [])

        ilst = iter(lst)
        self.assertEqual(m.mock_calls, [])

        self.assertEqual(next(ilst), m.a.transform.return_value)
        self.assertEqual(
            m.mock_calls,
            [mock.call.a.transform(mock_lang)]
        )

        # test repeat gets dont cause extra transform calls
        self.assertEqual(lst[0], m.a.transform.return_value)
        self.assertEqual(
            m.mock_calls,
            [mock.call.a.transform(mock_lang)]
        )

        self.assertEqual(
            list(ilst),
            [
                m.b.transform.return_value,
                m.c.transform.return_value
            ]
        )
