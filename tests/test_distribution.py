from unittest.mock import MagicMock

from models.containers.rocketsilo import RocketSilo
from services.distribution import expand_and_sort_items, find_open_silo, \
    first_fit_silo


def mock_silo(add_item_return):
    silo = RocketSilo()
    silo.add_item = MagicMock(return_value=add_item_return)
    return silo


class TestDistribution:
    item = {
        "name": "Item",
        "weight": 1
    }

    def test_item_expansion(self):
        items = [("transportbelt", 2), ("chemicalplant", 3)]
        expanded_items = expand_and_sort_items(items)
        assert len(expanded_items) == 5

    def test_item_sorting(self):
        items = [("transportbelt", 1), ("chemicalplant", 1)]
        expanded_items = expand_and_sort_items(items)
        assert expanded_items[0]['weight'] >= expanded_items[1]['weight']
        items_reversed = [("chemicalplant", 1), ("transportbelt", 1)]
        expanded_items_reversed = expand_and_sort_items(items_reversed)
        assert (expanded_items_reversed[0]['weight'] >=
                expanded_items_reversed[1]['weight'])

    def test_find_open_silo_when_item_fits(self):
        silo = mock_silo(True)
        assert find_open_silo([silo], self.item) is True

    def test_find_open_silo_when_item_not_fits(self):
        silos = [mock_silo(False), mock_silo(False), mock_silo(False)]
        assert find_open_silo(silos, self.item) is False

    def test_find_first_open_silo(self):
        silos = [mock_silo(False), mock_silo(True), mock_silo(True)]
        assert find_open_silo(silos, self.item) is True
        silos[1].add_item.assert_called_once_with(self.item)
        silos[2].add_item.assert_not_called()

    def test_first_fit_silo_when_item_fits(self):
        silos = [mock_silo(True)]
        first_fit_silo(silos, [self.item])
        silos[0].add_item.assert_called_once_with(self.item)
        assert len(silos) == 1

    def test_first_fit_silo_when_item_not_fits(self):
        silos = [mock_silo(False)]
        first_fit_silo(silos, [self.item])
        assert len(silos) == 2

    def test_items_fill_first_existing_silo(self):
        silos = [RocketSilo(), mock_silo(True)]
        items = [self.item, self.item]
        first_fit_silo(silos, items)
        assert len(silos) == 2
        assert silos[0].load == 2
        silos[1].add_item.assert_not_called()

    def test_items_fill_multiple_existing_silos(self):
        silos = [RocketSilo(), mock_silo(True)]
        item = {"weight": 350}
        items = [item, item, item]
        first_fit_silo(silos, items)
        assert len(silos) == 2
        assert silos[0].load == 700
        silos[1].add_item.assert_called_once_with(item)

    def test_items_fill_existing_silos_before_creating_new(self):
        silos = [mock_silo(False), RocketSilo()]
        items = [{"name": "Item", "weight": 1000}, self.item]
        first_fit_silo(silos, items)
        assert len(silos) == 3