from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo
from services.distribution import distribute_items
from services.initialize_setup import calculate_launch_cycles, group_items, \
    print_consolidated, print_distribution


def test_calculate_launch_cycles():
    silos = [RocketSilo()]
    num_silos = 1
    assert calculate_launch_cycles(silos, num_silos) == 1

    silos = [RocketSilo() for _ in range(10)]
    num_silos = 1
    assert calculate_launch_cycles(silos, num_silos) == 10

    silos = [RocketSilo() for _ in range(10)]
    num_silos = 2
    assert calculate_launch_cycles(silos, num_silos) == 5

    silos = [RocketSilo() for _ in range(15)]
    num_silos = 4
    assert calculate_launch_cycles(silos, num_silos) == 4

    silos = []
    num_silos = 3
    assert calculate_launch_cycles(silos, num_silos) == 0

    silos = [RocketSilo() for _ in range(5)]
    num_silos = 10
    assert calculate_launch_cycles(silos, num_silos) == 1

def test_group_item():
    grouped_items = group_items([ITEMS["pipe"]])
    assert len(grouped_items) == 1

def test_group_multiple_same_items():
    items = [ITEMS["transportbelt"] for _ in range(10)]
    grouped_items = group_items(items)
    assert len(grouped_items) == 1
    assert grouped_items[ITEMS["transportbelt"]["name"]] == 10

def test_group_multiple_single_items():
    items = [ITEMS["transportbelt"], ITEMS["chemicalplant"]]
    grouped_items = group_items(items)
    assert len(grouped_items) == 2
    assert grouped_items[ITEMS["transportbelt"]["name"]] == 1
    assert grouped_items[ITEMS["chemicalplant"]["name"]] == 1

def test_group_multiple_different_items():
    belts = [ITEMS["transportbelt"] for _ in range(18)]
    plants = [ITEMS["chemicalplant"] for _ in range(7)]
    foo = [{"name": "bar", "id": 1} for _ in range(21)]
    items = belts + plants + foo
    grouped_items = group_items(items)
    assert len(grouped_items) == 3
    assert grouped_items[ITEMS["transportbelt"]["name"]] == 18
    assert grouped_items[ITEMS["chemicalplant"]["name"]] == 7
    assert grouped_items["bar"] == 21

def test_group_items_sort_by_id():
    items = group_items([{"name": "a", "id": 3}, {"name": "b", "id": 1}, {"name": "c", "id": 2}])
    assert items == {"b": 1, "c": 1, "a": 1}

def test_print():
    items = [("transportbelt", 220), ("inserter", 25), ("pipetoground", 15),
             ("chemicalplant", 4), ("thruster", 6), ("crusher", 7)]
    silos = distribute_items(items)
    print_distribution(silos, 4)
    print_consolidated(silos, 4)