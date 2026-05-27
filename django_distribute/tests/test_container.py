from unittest import TestCase

from django_distribute.containers.chest import Chest
from django_distribute.containers.rocketsilo import RocketSilo
from django_distribute.data.items import ITEMS


class TestChestContainer(TestCase):
    def setUp(self) -> None:
        self.chest = Chest()
        self.belt = ITEMS["Transport belt"]

    def test_initialized_chest(self):
        self.assertFalse(self.chest.inventory, [])

    def test_add_item_to_chest(self):
        self.chest.add_item(self.belt)
        self.assertEqual(self.chest.inventory, [self.belt])

    def test_cannot_add_item_to_chest(self):
        self.chest.load = 48
        res = self.chest.add_item(self.belt)
        self.assertFalse(res)
        self.assertFalse(self.chest.inventory)

    def test_remove_item_from_chest(self):
        self.chest.add_item(self.belt)
        self.chest.remove_item(self.belt)
        self.assertFalse(self.chest.inventory)


class TestSiloContainer(TestCase):
    def setUp(self) -> None:
        self.silo = RocketSilo()
        self.belt = ITEMS["Transport belt"]

    def test_initialized_silo(self):
        self.assertFalse(self.silo.inventory)
        self.assertEqual(self.silo.capacity, 1000)
        self.assertFalse(self.silo.load)

    def test_add_item_to_silo(self):
        self.silo.add_item(self.belt)
        self.assertEqual(self.silo.inventory, [self.belt])

    def test_remove_item_from_silo(self):
        self.silo.add_item(self.belt)
        self.silo.remove_item(self.belt)
        self.assertFalse(self.silo.inventory)

    def test_silo_load(self):
        self.silo.add_item(self.belt)
        self.assertEqual(self.silo.load, self.belt["weight"])
        self.silo.remove_item(self.belt)
        self.assertFalse(self.silo.load)

    def test_add_overweight_item_to_silo(self):
        self.assertFalse(
            self.silo.add_item(
                {"weight": 1001, "stack_size": 1, "id": 1, "rocket_capacity": 1}
            )
        )

    def test_add_items_until_silo_overweight(self):
        heavy = {"weight": 350}
        self.assertTrue(self.silo.add_item(heavy))
        self.assertTrue(self.silo.add_item(heavy))
        self.assertFalse(self.silo.add_item(heavy))

    def test_add_many_light_items_to_silo(self):
        light = {"weight": 1}
        for _ in range(1000):
            self.silo.add_item(light)
        self.assertEqual(self.silo.load, self.silo.capacity)

    def test_silo_load_weight(self):
        self.silo.add_item(ITEMS["Artificial yumako soil"])
        val = 988 / 67
        self.assertEqual(self.silo.load, val)
