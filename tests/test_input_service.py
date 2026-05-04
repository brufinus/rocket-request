import pytest

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from data.items import ITEMS
from services.input_service import confirm_suggested_item, is_done_adding_items, transform_string


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

def test_confirm_suggested_item():
    assert confirm_suggested_item("y", "foobar") == "foobar"

def test_deny_suggested_item():
    assert confirm_suggested_item("n", "foobar") == ""

def test_confirm_suggested_item_malformed_input():
    assert confirm_suggested_item("foobar", "foobar") == ""
    assert confirm_suggested_item("  --Y-_ ", "foobar") == "foobar"