import pytest

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from data.items import ITEMS
from services.validation import is_insertable, parse_count


def test_parse_count():
    assert parse_count("1") == 1
    assert parse_count("5") == 5
    assert parse_count("20") == 20


def test_parse_count_non_int():
    with pytest.raises(ValueError, match=INPUT_INVALID_NUM):
        parse_count("foobar")


def test_parse_count_invalid_int():
    with pytest.raises(ValueError, match=INPUT_GREATER_ZERO):
        parse_count("0")
    with pytest.raises(ValueError, match=INPUT_GREATER_ZERO):
        parse_count("-1")


def test_is_valid_item():
    assert is_insertable("yumako", ITEMS) == True


def test_is_invalid_item():
    assert is_insertable("atomicbomb", ITEMS) == False


def test_is_valid_item_empty():
    assert is_insertable("", ITEMS) == False
