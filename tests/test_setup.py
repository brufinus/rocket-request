from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo
from services.initialize_setup import calculate_launch_cycles, condense_items


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

def test_condense_multiple_same_items():
    items = [ITEMS["transport_belt"] for _ in range(10)]
    condensed_items = condense_items(items)
    assert len(condensed_items) == 1
    assert condensed_items[ITEMS["transport_belt"]["name"]] == 10

def test_condense_multiple_single_items():
    items = [ITEMS["transport_belt"], ITEMS["chemical_plant"]]
    condensed_items = condense_items(items)
    assert len(condensed_items) == 2
    assert condensed_items[ITEMS["transport_belt"]["name"]] == 1
    assert condensed_items[ITEMS["chemical_plant"]["name"]] == 1

def test_condense_multiple_different_items():
    belts = [ITEMS["transport_belt"] for _ in range(18)]
    plants = [ITEMS["chemical_plant"] for _ in range(7)]
    foo = [{"name": "bar"} for _ in range(21)]
    items = belts + plants + foo
    condensed_items = condense_items(items)
    assert len(condensed_items) == 3
    assert condensed_items[ITEMS["transport_belt"]["name"]] == 18
    assert condensed_items[ITEMS["chemical_plant"]["name"]] == 7
    assert condensed_items["bar"] == 21