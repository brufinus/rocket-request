from hypothesis import given, strategies as st
import pytest

from django_distribute.services.helper import transform_string
from django_distribute.services.input_service import *


def test_transform_string():
    assert transform_string("ThIS   is-A-   - weird ST rIN-g  ") == "thisisaweirdstring"


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


@given(st.integers(min_value=1))
def test_request_valid_silo_count(n):
    pytest.MonkeyPatch().setattr("builtins.input", lambda _: f"{n}")
    assert request_silo_count() == n


@given(st.integers(max_value=0))
def test_request_invalid_silo_count(n):
    inputs = iter([n, "1"])
    pytest.MonkeyPatch().setattr("builtins.input", lambda _: next(inputs))
    assert request_silo_count() == 1


def test_request_str_silo_count():
    inputs = iter(["foobar", "1"])
    pytest.MonkeyPatch().setattr("builtins.input", lambda _: next(inputs))
    assert request_silo_count() == 1


def test_request_items():
    inputs = iter(
        [
            "belt",
            "1",
            "pipe",
            "0",
            "-1",
            "100",
            "atomicbomb",
            "yummako",
            "y",
            "15",
            "done",
        ]
    )
    pytest.MonkeyPatch().setattr("builtins.input", lambda _: next(inputs))
    assert request_items() == [("transportbelt", 1), ("pipe", 100), ("yumako", 15)]
