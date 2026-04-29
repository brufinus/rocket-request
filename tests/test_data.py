from data.items import ITEMS


class TestItems:
    def test_item_exists(self):
        assert "transport_belt" in ITEMS

    def test_item_not_exists(self):
        assert "banana" not in ITEMS

    def test_weight_calculation(self):
        belt = ITEMS["transport_belt"]
        assert belt["weight"] == 1000 / belt["rocket_capacity"]
