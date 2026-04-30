from data.items import ITEMS
from models.containers.Chest import Chest
from models.containers.RocketSilo import RocketSilo


class TestContainer:
    def setup_method(self):
        self.chest = Chest()
        self.silo = RocketSilo()
        self.belt = ITEMS['transport_belt']

    def test_initialized_chest(self):
        assert self.chest.inventory == []

    def test_add_item_to_chest(self):
        self.chest.add_item(self.belt)
        assert self.chest.inventory == [self.belt]

    def test_remove_item_from_chest(self):
        self.chest.add_item(self.belt)
        self.chest.remove_item(self.belt)
        assert self.chest.inventory == []

    def test_initialized_silo(self):
        assert self.silo.inventory == []
        assert self.silo.capacity == 1000
        assert self.silo.load == 0

    def test_add_item_to_silo(self):
        self.silo.add_item(self.belt)
        assert self.silo.inventory == [self.belt]

    def test_remove_item_from_silo(self):
        self.silo.add_item(self.belt)
        self.silo.remove_item(self.belt)
        assert self.silo.inventory == []

    def test_silo_load(self):
        self.silo.add_item(self.belt)
        assert self.silo.load == self.belt['weight']
        self.silo.remove_item(self.belt)
        assert self.silo.load == 0

    def test_add_overweight_item_to_silo(self):
        assert self.silo.add_item({"weight": 1001}) == False

    def test_add_items_until_silo_overweight(self):
        heavy = {"weight": 350}
        assert self.silo.add_item(heavy)
        assert self.silo.add_item(heavy) == True
        assert self.silo.add_item(heavy) == False

    def test_add_many_light_items_to_silo(self):
        light = {"weight": 1}
        for i in range(1000):
            self.silo.add_item(light)
        assert self.silo.load == self.silo.capacity