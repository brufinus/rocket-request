from unittest import TestCase

import pytest
from hypothesis import given
from hypothesis import strategies as st

from django_distribute.services.helper import transform_string
from django_distribute.services.input_service import *


class TestInputService(TestCase):
    def test_transform_string(self):
        self.assertEqual(
            transform_string("ThIS   is-A-   - weird ST rIN-g  "), "thisisaweirdstring"
        )

    def test_is_done_adding_no_items(self):
        self.assertFalse(is_done_adding_items("done", []))

    def test_is_done_adding_with_items(self):
        self.assertTrue(is_done_adding_items("done", [("foo", 1)]))

    def test_is_not_done_adding_no_items(self):
        self.assertFalse(is_done_adding_items("foobar", []))

    def test_is_not_done_adding_with_items(self):
        self.assertFalse(is_done_adding_items("foobar", [("foo", 1)]))

    def test_is_not_done_adding_with_existing_item(self):
        self.assertFalse(is_done_adding_items("foobar", [("foobar", 1)]))

    def test_confirm_suggested_item(self):
        self.assertEqual(confirm_suggested_item("y", "foobar"), "foobar")

    def test_deny_suggested_item(self):
        self.assertFalse(confirm_suggested_item("n", "foobar"))

    def test_confirm_suggested_item_malformed_input(self):
        self.assertFalse(confirm_suggested_item("foobar", "foobar"))
        self.assertEqual(confirm_suggested_item("  --Y-_ ", "foobar"), "foobar")

    @given(st.integers(min_value=1))
    def test_request_valid_silo_count(self, n):
        pytest.MonkeyPatch().setattr("builtins.input", lambda _: f"{n}")
        self.assertEqual(request_silo_count(), n)

    @given(st.integers(max_value=0))
    def test_request_invalid_silo_count(self, n):
        inputs = iter([n, "1"])
        pytest.MonkeyPatch().setattr("builtins.input", lambda _: next(inputs))
        self.assertEqual(request_silo_count(), 1)

    def test_request_str_silo_count(self):
        inputs = iter(["foobar", "1"])
        pytest.MonkeyPatch().setattr("builtins.input", lambda _: next(inputs))
        self.assertEqual(request_silo_count(), 1)

    def test_request_items(self):
        inputs = iter(
            [
                "belt",
                "1",
                "pipe",
                "0",
                "-1",
                "100",
                "Atomic bomb",
                "yummako",
                "y",
                "15",
                "done",
            ]
        )
        pytest.MonkeyPatch().setattr("builtins.input", lambda _: next(inputs))
        self.assertEqual(
            request_items(), [("Transport belt", 1), ("Pipe", 100), ("Yumako", 15)]
        )
