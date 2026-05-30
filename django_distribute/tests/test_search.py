from unittest import TestCase

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
    def test_search_item_by_key(self):
        self.assertGreater(len(search_item("item1", dictionary)), 0)

    def test_search_item_by_keyword(self):
        self.assertGreater(len(search_item("alias", dictionary)), 0)
        self.assertGreater(len(search_item("foo", dictionary)), 0)
        self.assertGreater(len(search_item("bar", dictionary)), 0)

    def test_validate_correct_item_by_keyword(self):
        self.assertEqual(search_item("belt", ITEMS), "Transport belt")

    def test_invalid_item(self):
        self.assertFalse(len(search_item("pootis", dictionary)))

    def test_search_similar_item(self):
        self.assertEqual(search_similar_item("item", dictionary), "item1")
        thisdict = {"grapple": "0.73", "orange": "0.4", "apple": "0.89"}
        self.assertEqual(search_similar_item("aple", thisdict), "apple")

    def test_get_with_confidence(self):
        """Returns sword as it is above the confidence threshold."""
        thisdict = {"sword": "0.89", "word": "1.0"}
        self.assertEqual(search_similar_item("word", thisdict), "sword")

    def test_no_similar_items(self):
        self.assertFalse(search_similar_item("banana", dictionary))

    def test_search_similar_items_no_item(self):
        self.assertFalse(search_similar_item("", dictionary))

    def test_search_similar_items_empty_dict(self):
        self.assertFalse(search_similar_item("foobar", {}))

    def test_search_similar_items_of_same_ratio(self):
        thisdict = {"bworde": "0.8", "sworde": "0.8"}
        self.assertEqual(search_similar_item("word", thisdict), "bworde")

    def test_search_coordinator_no_matches(self):
        self.assertEqual(search_coordinator("foobar", ITEMS), ("", False))

    def test_search_coordinator_similar(self):
        self.assertEqual(
            search_coordinator("electonic crcut", ITEMS), ("Electronic circuit", True)
        )

    def test_search_coordinator_match(self):
        item_name = "Advanced circuit"
        self.assertEqual(search_coordinator(item_name, ITEMS), (item_name, False))
    
    def test_search_transformed_item(self):
        self.assertEqual(search_item("transportbelt", ITEMS), "Transport belt")
