import math

from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo


def print_distribution(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of items across available silos.

    :param silos: List of silos with items.
    :param num_silos: Number of available silos.
    :return: None
    """
    print(f"\nTotal launches required: {len(silos)}")
    cycles = calculate_launch_cycles(silos, num_silos)
    print(f"Required launch cycles: {cycles}")

    silo_index = 0
    for i in range(cycles):
        print(f"Cycle {i + 1}:")
        for j in range(num_silos):
            if silo_index >= len(silos):
                break
            print(f"\n\tSilo {j + 1} ({silos[silo_index].load}"
                  f"/{silos[silo_index].capacity} kg):")
            print_item_header()
            print_grouped_items(group_items(silos[silo_index].inventory))
            silo_index += 1


def print_consolidated(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of items consolidated across available silos.

    :param silos: List of silos with items.
    :param num_silos: Number of available silos.
    :return: None
    """
    print("\nConsolidated silo contents:")
    silo_index = 0
    while silo_index < num_silos:
        print(f"\n\tSilo {silo_index + 1}:")
        print_item_header()
        i = silo_index
        while i < len(silos):
            print_grouped_items(group_items(silos[i].inventory))
            i += num_silos
        silo_index += 1


def print_grouped_items(items: dict[str, int]) -> None:
    """
    Prints the formatted name and count for each grouped item.
    
    :param items: Dictionary of grouped items
    :return: None
    """
    for i in items:
        print(f"\t\t{i:<{get_col_width()}}{items[i]:>10}")


def print_item_header() -> None:
    """Prints the Item, Count header."""
    col_width = get_col_width()
    print(f"\t\t{"Item":<{col_width}}{"Count":>10}")
    print(f"\t\t{"-" * (col_width + 10)}")


def get_col_width() -> int:
    """Returns a column width for output padding."""
    return len(max(ITEMS, key=len)) + 2


def group_items(items: list[dict[str, str | int]]) -> dict[str, int]:
    """
    Consolidate and group together items by name and their count.

    :param items: List of items in the silo.
    :return: Consolidated list of each item and their count.
    :rtype: dict
    """
    grouped_items: dict[str, int] = {}
    for item in items:
        grouped_items.update(
            {str(item["name"]): grouped_items.get(str(item["name"]), 0) + 1})
    return grouped_items


def calculate_launch_cycles(silos: list[RocketSilo], num_silos: int) -> int:
    """
    Calculates the number launch cycles required.

    :param silos: List of silos with items.
    :param num_silos: Number of available silos.
    :return: Number of launch cycles.
    :rtype: int
    """
    return math.ceil(len(silos) / num_silos)
