import pytest

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from data.items import ITEMS
from services.input_service import is_done_adding_items, transform_string


def test_transform_string():
    assert transform_string("ThIS   is-A-   - weird ST rIN-g  ") \
        == "thisisaweirdstring"

def test_is_done_adding_no_items():
    assert is_done_adding_items("done", []) == False

def test_is_done_adding_with_items():
    assert is_done_adding_items("done", [("foo", 1)]) == True

def test_is_not_done_adding_no_items():
    assert is_done_adding_items("foobar", []) == False

def test_is_not_done_adding_with_items():
    assert is_done_adding_items("foobar", [("foo", 1)]) == False

def test_is_not_done_adding_with_existing_item():
    assert is_done_adding_items("foobar", [("foobar", 1)]) == False
