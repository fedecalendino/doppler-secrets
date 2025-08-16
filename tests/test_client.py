from datetime import datetime, date, timezone
from unittest import TestCase
from uuid import UUID

import ddt
from doppler import Doppler

TEST_CASES = (
    ("HELLO", "WORLD"),
    ("LIST", ["item1", "item2", "item3"]),
    ("SEVEN", 7),
    ("PI", 3.14),
    ("TRUE", True),
    ("FALSE", False),
    ("DATE", date(year=1999, month=12, day=31)),
    ("DATETIME", datetime(year=1999, month=12, day=31, hour=23, minute=59, second=59, tzinfo=timezone.utc)),
    ("JSON", {"key": "value", "number": 42}),
    ("UUID", UUID("cabe3b6d-d623-484c-acd7-888beb79c1a9")),
)


@ddt.ddt
class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doppler = Doppler(
            "doppler-secrets",
            "test",
            defaults={
                "ABC": 123,
            },
        )

    @ddt.data(*TEST_CASES)
    @ddt.unpack
    def test_get(self, name: str, expected: object):
        value = self.doppler.get(name)
        self.assertEqual(expected, value)

    @ddt.data(*TEST_CASES)
    @ddt.unpack
    def test_getattribute(self, name: str, expected: object):
        value = getattr(self.doppler, name)
        self.assertEqual(expected, value)

    @ddt.data(*TEST_CASES)
    @ddt.unpack
    def test_getitem(self, name: str, expected: object):
        value = self.doppler[name]
        self.assertEqual(expected, value)

    def test_json(self):
        json = self.doppler.get("JSON")

        self.assertIsInstance(json, dict)
        self.assertEqual(json.key, "value")
        self.assertEqual(json.number, 42)

        with self.assertRaises(KeyError) as exc:
            print(json.random)

        self.assertEqual(str(exc.exception), "'JSON.random is not a valid secret'")

    def test_defaults(self):
        self.assertEqual(123, self.doppler.get("ABC"))
        self.assertEqual(123, self.doppler.ABC)
        self.assertEqual(123, self.doppler["ABC"])
