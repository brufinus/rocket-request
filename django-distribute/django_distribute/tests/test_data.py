from pathlib import Path
from unittest import TestCase

from django_distribute.data.constants import ITEM_ID
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

    def test_validate_data(self):
        """Item data matches in-game data."""
        datafile = Path(__file__).parent / "items.txt"
        with open(datafile) as f:
            items = f.read().splitlines()
        for item in ITEMS:
            item_slug = item.lower().replace(" ", "-")
            self.assertIn(item_slug, items)

    def test_validate_ids(self):
        """Each item has a unique ID."""
        ids = []
        for key in ITEMS:
            id = ITEMS[key][ITEM_ID]
            self.assertNotIn(id, ids)
            ids.append(id)
