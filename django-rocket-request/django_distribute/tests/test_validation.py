from unittest import TestCase

import pytest

from django_distribute.data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from django_distribute.data.items import ITEMS
from django_distribute.services.validation import is_insertable, parse_count


class TestValidation(TestCase):
    def test_parse_count(self):
        self.assertEqual(parse_count("1"), 1)
        self.assertEqual(parse_count("5"), 5)
        self.assertEqual(parse_count("20"), 20)

    def test_parse_count_non_int(self):
        with pytest.raises(ValueError, match=INPUT_INVALID_NUM):
            parse_count("foobar")

    def test_parse_count_invalid_int(self):
        with pytest.raises(ValueError, match=INPUT_GREATER_ZERO):
            parse_count("0")
        with pytest.raises(ValueError, match=INPUT_GREATER_ZERO):
            parse_count("-1")

    def test_is_valid_item(self):
        self.assertTrue(is_insertable("Yumako", ITEMS))

    def test_is_invalid_item(self):
        self.assertFalse(is_insertable("Atomic bomb", ITEMS))

    def test_is_valid_item_empty(self):
        self.assertFalse(is_insertable("", ITEMS))
