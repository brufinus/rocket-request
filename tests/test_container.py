from data.items import ITEMS
from models.containers.Chest import Chest


class TestContainer:
    def setup_method(self):
        self.chest = Chest()

    def test_initialized_chest(self):
        assert self.chest.inventory == []

    def test_add_item_to_chest(self):
        self.chest.add_item(ITEMS['transport_belt'])
        assert self.chest.inventory == [ITEMS['transport_belt']]

    def test_remove_item_from_chest(self):
        self.chest.add_item(ITEMS['transport_belt'])
        self.chest.remove_item(ITEMS['transport_belt'])
        assert self.chest.inventory == []