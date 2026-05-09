from django_distribute.data.items import ITEMS, make_item


def test_item_exists():
    assert "transportbelt" in ITEMS


def test_item_not_exists():
    assert "banana" not in ITEMS


def test_weight_calculation():
    belt = ITEMS["transportbelt"]
    assert belt["weight"] == 1000 / belt["rocket_capacity"]


def test_custom_weight():
    items = {"testitem": make_item("Test item", 100, 21, 0, [], 5.0)}
    assert items["testitem"]["weight"] == 5.0
