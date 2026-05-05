from data.items import ITEMS
from models.containers.rocketsilo import RocketSilo
from services.distribution import distribute_items
from services.initialize_setup import (
    build_distribution,
    calculate_launch_cycles,
    get_formatted_load,
    group_items,
    print_consolidated,
    print_distribution,
    get_load_visualization,
)


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
    items = group_items(
        [{"name": "a", "id": 3}, {"name": "b", "id": 1}, {"name": "c", "id": 2}]
    )
    assert items == {"b": 1, "c": 1, "a": 1}


# def test_print():
#     items = [("transportbelt", 220), ("inserter", 25), ("pipetoground", 15),
#              ("chemicalplant", 4), ("thruster", 6), ("crusher", 7)]
#     silos = distribute_items(items)
#     print_distribution(silos, 4)
#     print_consolidated(silos, 4)


def test_print_full_setup():
    # Run with -s flag.
    items = [
        ("transportbelt", 194),
        ("inserter", 42),
        ("pipe", 36),
        ("efficiencymodule2", 32),
        ("efficiencymodule", 24),
        ("undergroundbelt", 18),
        ("longhandedinserter", 17),
        ("gunturret", 14),
        ("solarpanel", 12),
        ("electricfurnace", 10),
        ("accumulator", 9),
        ("chemicalplant", 8),
        ("asteroidcollector", 8),
        ("fastinserter", 7),
        ("splitter", 6),
        ("fastundergroundbelt", 4),
        ("pipetoground", 4),
        ("crusher", 4),
        ("storagetank", 3),
        ("thruster", 3),
        ("assemblingmachine2", 2),
        ("uraniumroundsmagazine", 100),
    ]
    silos = distribute_items(items)
    print_distribution(silos, 8)


def test_full_load_visualization():
    assert get_load_visualization(1000, 1000) == "[██████████]"


def test_half_load_visualization():
    assert get_load_visualization(500, 1000) == "[█████░░░░░]"


def test_partial_load_visualization():
    assert get_load_visualization(300, 1000) == "[███░░░░░░░]"


def test_quarter_load_visualization():
    assert get_load_visualization(250, 1000) == "[███░░░░░░░]"


def test_mid_rounding_load_visualization():
    assert get_load_visualization(501, 1000) == "[█████░░░░░]"


def test_big_rounding_load_visualization():
    assert get_load_visualization(774, 1000) == "[████████░░]"


def test_empty_load_visualization():
    assert get_load_visualization(0, 1000) == "[░░░░░░░░░░]"


def test_get_formatted_load_whole():
    assert get_formatted_load(100.0) == "100"
    assert get_formatted_load(900.0) == "900"


def test_get_formatted_load_decimal():
    assert get_formatted_load(8.251) == "8.3"
    assert get_formatted_load(100.8574) == "100.9"


def test_build_distribution_one_cycle():
    silos = [RocketSilo(), RocketSilo()]
    silos[0].add_item(ITEMS["nuclearreactor"])
    silos[1].add_item(ITEMS["thruster"])
    assert build_distribution(silos, 2) == [[{"Nuclear reactor": 1}, {"Thruster": 1}]]


def test_build_distribution_more_silos_than_available():
    # Multiple cycles
    silos = [RocketSilo(), RocketSilo(), RocketSilo()]
    silos[0].add_item(ITEMS["nuclearreactor"])
    silos[1].add_item(ITEMS["thruster"])
    for _ in range(8):
        silos[1].add_item(ITEMS["crusher"])
    for _ in range(2):
        silos[2].add_item(ITEMS["thruster"])
    assert build_distribution(silos, 2) == [
        [{"Nuclear reactor": 1}, {"Crusher": 8, "Thruster": 1}],
        [{"Thruster": 2}],
    ]


def test_build_distribution_less_silos_than_available():
    # Only one cycle
    silos = [RocketSilo(), RocketSilo(), RocketSilo()]
    silos[0].add_item(ITEMS["nuclearreactor"])
    silos[1].add_item(ITEMS["thruster"])
    for _ in range(8):
        silos[1].add_item(ITEMS["crusher"])
    for _ in range(2):
        silos[2].add_item(ITEMS["thruster"])
    assert build_distribution(silos, 10) == [
        [{"Nuclear reactor": 1}, {"Crusher": 8, "Thruster": 1}, {"Thruster": 2}]
    ]


def test_build_distribution_empty():
    assert build_distribution([], 3) == []
