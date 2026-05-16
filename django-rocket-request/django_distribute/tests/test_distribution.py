from unittest import TestCase
from unittest.mock import MagicMock

from django_distribute.containers.rocketsilo import RocketSilo
from django_distribute.data.items import ITEMS, make_item
from django_distribute.services.distribution import (
    expand_and_sort_items,
    find_open_silo,
    first_fit_silo,
)


def mock_silo(add_item_return):
    silo = RocketSilo()
    silo.add_item = MagicMock(return_value=add_item_return)
    return silo


class TestDistribution(TestCase):
    item = make_item(1, 100, 1)

    def test_item_expansion(self):
        """Items are added to a list as many times as their count."""
        items = {"Transport belt": 2, "Chemical plant": 3}
        expected1 = [ITEMS["Chemical plant"] for _ in range(3)]
        expected2 = [ITEMS["Transport belt"] for _ in range(2)]
        expanded_items = expand_and_sort_items(items)
        self.assertEqual(len(expanded_items), 5)
        self.assertEqual(expanded_items, expected1 + expected2)

    def test_item_sorting(self):
        """Items are sorted heaviest to lightest."""
        items = {"Pipe": 1, "Transport belt": 1, "Chemical plant": 1}
        expanded_items = expand_and_sort_items(items)
        self.assertGreater(expanded_items[0]["weight"], expanded_items[1]["weight"])
        items_reversed = {"Chemical plant": 1, "Transport belt": 1, "Pipe": 1}
        expanded_items_reversed = expand_and_sort_items(items_reversed)
        self.assertGreater(
            expanded_items_reversed[0]["weight"], expanded_items_reversed[1]["weight"]
        )
        self.assertEqual(expanded_items, expanded_items_reversed)

    def test_find_open_silo_when_item_fits(self):
        """An item is added when there is space."""
        silo = mock_silo(True)
        self.assertTrue(find_open_silo([silo], self.item))

    def test_find_open_silo_when_item_not_fits(self):
        """No item is added when there is no space."""
        silos = [mock_silo(False), mock_silo(False), mock_silo(False)]
        self.assertFalse(find_open_silo(silos, self.item))

    def test_find_first_open_silo(self):
        """The item is added to the first open silo."""
        silos = [mock_silo(False), mock_silo(True), mock_silo(True)]
        self.assertTrue(find_open_silo(silos, self.item))
        silos[1].add_item.assert_called_once_with(self.item)
        silos[2].add_item.assert_not_called()

    def test_first_fit_silo_when_item_fits(self):
        """The item fits into the silo."""
        silos = [mock_silo(True)]
        first_fit_silo(silos, [self.item])
        silos[0].add_item.assert_called_once_with(self.item)
        self.assertEqual(len(silos), 1)

    def test_first_fit_silo_when_item_not_fits(self):
        """The item does not fit into any silo, so new one is opened."""
        silos = [mock_silo(False)]
        first_fit_silo(silos, [self.item])
        self.assertEqual(len(silos), 2)

    def test_items_fill_first_existing_silo(self):
        """Existing silos are filled first."""
        silos = [RocketSilo(), mock_silo(True)]
        items = [self.item, self.item]
        first_fit_silo(silos, items)
        self.assertEqual(len(silos), 2)
        self.assertEqual(silos[0].load, 20.0)
        silos[1].add_item.assert_not_called()

    def test_items_fill_multiple_existing_silos(self):
        """Items fill space over multiple existing silos."""
        silos = [RocketSilo(), mock_silo(True)]
        item = {"weight": 350}
        items = [item, item, item]
        first_fit_silo(silos, items)
        self.assertEqual(len(silos), 2)
        self.assertEqual(silos[0].load, 700)
        silos[1].add_item.assert_called_once_with(item)

    def test_items_fill_existing_silos_before_creating_new(self):
        """Items fill existing silos before creating a new one."""
        silos = [mock_silo(False), RocketSilo()]
        items = [{"name": "Item", "weight": 1000}, self.item]
        first_fit_silo(silos, items)
        self.assertEqual(len(silos), 3)
