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
        # Calculate total extra digits.
        separators = "═" * int(math.log10(i + 1) + math.log10(cycles) + 1)
        print(f"╔═══════════════════════{separators}╗")
        print(f"║      Cycle {i + 1} of {cycles}      ║")
        print(f"╚═══════════════════════{separators}╝")
        for j in range(num_silos):
            if silo_index >= len(silos):
                break
            rounded_load = "{:.1f}".format(silos[silo_index].load)
            print(f"\n\tSilo {j + 1} ({rounded_load}"
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
        superlist = []  # Running list of silo items
        while i < len(silos):
            superlist += silos[i].inventory
            i += num_silos
        print_grouped_items(group_items(superlist))
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


def group_items(items: list[dict[str, str | float]]) -> dict[str, int]:
    """
    Consolidate and group together items by name, sorted by item id.

    :param items: List of items in the silo.
    :return: Consolidated, sorted item name and counts.
    :rtype: dict[str, int]
    """
    grouped_items: dict[str, int] = {}
    ids = []
    for item in items:
        ids.append(item["id"])
    ids.sort()
    for id in ids:
        # Get item name using id.
        name = str([x["name"] for x in items if id == x["id"]][0])
        # Set item or increment its count.
        grouped_items.update({name: grouped_items.get(name, 0) + 1})
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
