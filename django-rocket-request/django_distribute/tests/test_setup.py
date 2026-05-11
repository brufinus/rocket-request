from hypothesis import given
from hypothesis import strategies as st

from django_distribute.containers.rocketsilo import RocketSilo
from django_distribute.data.items import ITEMS, make_item
from django_distribute.services.distribution import distribute_items
from django_distribute.services.helper import get_formatted_float
from django_distribute.services.initialize_setup import (
    build_consolidated_invs,
    build_consolidated_load,
    build_distribution,
    calculate_launch_cycles,
    get_consolidated_slots,
    group_items,
)
from django_distribute.services.output_service import (
    get_load_visualization,
    print_consolidated,
    print_distribution,
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
    grouped_items = group_items([ITEMS["Pipe"]], ITEMS)
    assert len(grouped_items) == 1


def test_group_multiple_same_items():
    items = [ITEMS["Transport belt"] for _ in range(10)]
    grouped_items = group_items(items, ITEMS)
    assert len(grouped_items) == 1
    assert grouped_items["Transport belt"] == 10


def test_group_multiple_single_items():
    items = [ITEMS["Transport belt"], ITEMS["Chemical plant"]]
    grouped_items = group_items(items, ITEMS)
    assert len(grouped_items) == 2
    assert grouped_items["Transport belt"] == 1
    assert grouped_items["Chemical plant"] == 1


def test_group_multiple_different_items():
    belts = [ITEMS["Transport belt"] for _ in range(18)]
    plants = [ITEMS["Chemical plant"] for _ in range(7)]
    pipes = [ITEMS["Pipe"] for _ in range(21)]
    items = belts + plants + pipes
    grouped_items = group_items(items, ITEMS)
    assert len(grouped_items) == 3
    assert grouped_items["Transport belt"] == 18
    assert grouped_items["Chemical plant"] == 7
    assert grouped_items["Pipe"] == 21


def test_group_items_sort_by_id():
    items = group_items(
        [make_item(1, 1, 3), make_item(1, 1, 1), make_item(1, 1, 2)],
        {"a": make_item(1, 1, 3), "b": make_item(1, 1, 1), "c": make_item(1, 1, 2)},
    )
    assert items == {"b": 1, "c": 1, "a": 1}


# def test_print():
#     items = [("Transport belt", 220), ("inserter", 25), ("pipetoground", 15),
#              ("Chemical plant", 4), ("Thruster", 6), ("Crusher", 7)]
#     silos = distribute_items(items)
#     print_distribution(silos, 4)
#     print_consolidated(silos, 4)


def test_print_full_setup():
    # Run with -s flag.
    items = {"Transport belt": 194, "Inserter": 42, "Pipe": 36}
    silos = distribute_items(items)
    print_distribution(silos, 2, ITEMS)


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


def test_get_formatted_float_whole():
    assert get_formatted_float(100.0) == "100"
    assert get_formatted_float(900.0) == "900"


def test_get_formatted_float_decimal():
    assert get_formatted_float(8.251) == "8.3"
    assert get_formatted_float(100.8574) == "100.9"


def test_build_distribution_one_cycle():
    silos = [RocketSilo(), RocketSilo()]
    silos[0].add_item(ITEMS["Nuclear reactor"])
    silos[1].add_item(ITEMS["Thruster"])
    assert build_distribution(silos, 2, ITEMS) == [
        [{"Nuclear reactor": 1}, {"Thruster": 1}]
    ]


def test_build_distribution_more_silos_than_available():
    # Multiple cycles
    silos = [RocketSilo(), RocketSilo(), RocketSilo()]
    silos[0].add_item(ITEMS["Nuclear reactor"])
    silos[1].add_item(ITEMS["Thruster"])
    for _ in range(8):
        silos[1].add_item(ITEMS["Crusher"])
    for _ in range(2):
        silos[2].add_item(ITEMS["Thruster"])
    assert build_distribution(silos, 2, ITEMS) == [
        [{"Nuclear reactor": 1}, {"Crusher": 8, "Thruster": 1}],
        [{"Thruster": 2}],
    ]


def test_build_distribution_less_silos_than_available():
    # Only one cycle
    silos = [RocketSilo(), RocketSilo(), RocketSilo()]
    silos[0].add_item(ITEMS["Nuclear reactor"])
    silos[1].add_item(ITEMS["Thruster"])
    for _ in range(8):
        silos[1].add_item(ITEMS["Crusher"])
    for _ in range(2):
        silos[2].add_item(ITEMS["Thruster"])
    assert build_distribution(silos, 10, ITEMS) == [
        [{"Nuclear reactor": 1}, {"Crusher": 8, "Thruster": 1}, {"Thruster": 2}]
    ]


def test_build_distribution_empty():
    assert build_distribution([], 3, ITEMS) == []


@given(st.integers(1, 1000), st.integers(1, 1000))
def test_build_consolidated_load(n, s):
    silos = []
    for val in n, s:
        silo = RocketSilo()
        silo.load = val
        silos.append(silo)
    assert build_consolidated_load(silos, 1) == [f"{n + s}"]


def test_build_consolidated_invs():
    silos = []
    for val in [ITEMS["Pipe"]], [ITEMS["Pipe"]], [ITEMS["Car"]]:
        silo = RocketSilo()
        silo.inventory = val
        silos.append(silo)
    assert build_consolidated_invs(silos, 1, ITEMS) == [{"Car": 1, "Pipe": 2}]


@given(st.integers(1, 10000), st.integers())
def test_get_consolidated_slots(n, s):
    silos = [RocketSilo() for _ in range(n)]
    assert len(get_consolidated_slots(silos, 1)) == 1
