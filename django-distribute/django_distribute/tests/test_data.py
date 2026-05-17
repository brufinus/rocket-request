from unittest import TestCase

from django_distribute.data.items import ITEMS, make_item


class TestItemData(TestCase):
    def test_item_exists(self):
        self.assertIn("Transport belt", ITEMS)

    def test_item_not_exists(self):
        self.assertNotIn("banana", ITEMS)

    def test_weight_calculation(self):
        belt = ITEMS["Transport belt"]
        self.assertEqual(belt["weight"], 1000 / belt["rocket_capacity"])

    def test_custom_weight(self):
        items = {"testitem": make_item(100, 21, 0, [], 5.0)}
        self.assertEqual(items["testitem"]["weight"], 5.0)
