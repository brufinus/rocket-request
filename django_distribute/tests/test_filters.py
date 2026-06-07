from unittest import TestCase

from django_distribute.templatetags.distribute_filters import filter_range


class TestFilters(TestCase):
    def test_range_filter(self):
        """The custom range filter returns a Python range."""
        self.assertEqual(filter_range(0, 10), range(0, 10))
        self.assertEqual(filter_range(5, 7), range(5, 7))

    def test_range_filter_invalid_inputs(self):
        """The custom range filter returns an empty array on invalid inputs."""
        self.assertEqual(filter_range("foo", "bar"), [])
        self.assertEqual(filter_range("10", "0"), [])
