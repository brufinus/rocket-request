import pytest

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from services.validation import parse_silo_count


def test_parse_silo_count():
    assert parse_silo_count("1") == 1
    assert parse_silo_count("5") == 5
    assert parse_silo_count("20") == 20

def test_parse_silo_count_non_int():
    with pytest.raises(ValueError, match=INPUT_INVALID_NUM):
        parse_silo_count("foobar")

def test_parse_silo_count_invalid_int():
    with pytest.raises(ValueError, match=INPUT_GREATER_ZERO):
        parse_silo_count("0")
    with pytest.raises(ValueError, match=INPUT_GREATER_ZERO):
        parse_silo_count("-1")