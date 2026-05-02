from data.items import ITEMS, make_item


class TestItems:
    def test_item_exists(self):
        assert "transportbelt" in ITEMS

    def test_item_not_exists(self):
        assert "banana" not in ITEMS

    def test_weight_calculation(self):
        belt = ITEMS["transportbelt"]
        assert belt["weight"] == 1000 / belt["rocket_capacity"]
    
    def test_custom_weight(self):
        items = {"testitem": make_item("Test item", 100, 21, 0, [], 5.0)}
        assert items["testitem"]["weight"] == 5.0
