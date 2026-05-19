from django.test import TestCase

from django_distribute.data.items import ITEMS
from django_distribute.services.search import (
    search_coordinator,
    search_item,
    search_similar_item,
)

dictionary = {
    "item1": {"keywords": ["alias"]},
    "somelongitemname": {"keywords": ["foo", "bar"]},
}


class TestSearch(TestCase):
    fixtures = ["items"]

    def test_search_item_by_name(self):
        item = "Transport belt"
        self.assertEqual(search_item(item), item)

    def test_search_item_by_keyword(self):
        self.assertEqual(search_item("belt"), "Transport belt")
        self.assertEqual(search_item("chemplant"), "Chemical plant")

    def test_validate_correct_item_by_keyword(self):
        self.assertEqual(search_item("belt"), "Transport belt")

    def test_invalid_item(self):
        self.assertFalse(len(search_item("pootis")))

    def test_search_similar_item(self):
        self.assertEqual(
            search_similar_item("tansprotblt"), "Transport belt"
        )

    def test_get_with_confidence(self):
        self.assertEqual(
            search_similar_item("cryogenic pant"), "Cryogenic plant"
        )

    def test_no_similar_items(self):
        self.assertFalse(search_similar_item("banana"))

    def test_search_similar_items_no_item(self):
        self.assertFalse(search_similar_item(""))

    def test_search_similar_items_empty_dict(self):
        self.assertFalse(search_similar_item("foobar"))

    def test_search_similar_items_of_same_ratio(self):
        self.assertEqual(search_similar_item("stong"), "Stone")
        self.assertEqual(search_similar_item("stonb"), "Stone")

    def test_search_coordinator_no_matches(self):
        self.assertEqual(search_coordinator("foobar"), ("", False))

    def test_search_coordinator_similar(self):
        self.assertEqual(
            search_coordinator("electonic crcut"), ("Electronic circuit", True)
        )

    def test_search_coordinator_match(self):
        item_name = "Advanced circuit"
        self.assertEqual(search_coordinator(item_name), (item_name, False))

    def test_search_transformed_item(self):
        self.assertEqual(search_item("transportbelt"), "Transport belt")
