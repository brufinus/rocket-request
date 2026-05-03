from decimal import ROUND_HALF_UP, Decimal
import math

from data.item import Item
from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo


def print_distribution(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of items across available silos.

    :param list[RocketSilo] silos: List of silos.
    :param int num_silos: Number of available silos.
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
            print(f"\n\tSilo {j + 1} {get_load_visualization(
                silos[silo_index].load,
                RocketSilo.CAPACITY)} ({get_formatted_load(
                    silos[silo_index].load)}"
                  f"/{silos[silo_index].capacity} kg):")
            print_item_header()
            print_grouped_items(group_items(silos[silo_index].inventory))
            silo_index += 1


def get_formatted_load(load: float) -> str:
    """
    Formats the load to a string.

    This method rounds the loadto the first decimal place
    or to the whole number if there are no decimals.

    :param float load: The load to format.
    :return: The formatted load.
    :rtype: str
    """
    if load % 1 == 0:
        return f"{int(load)}"
    return "{:.1f}".format(load)


def get_load_visualization(load: float, capacity: int) -> str:
    """
    Returns a visualization of the silo load in progress bar format.

    Example: [█████░░░░░] for 50% load.

    :param float load: The current load of the silo.
    :param int capacity: The maximum capacity of the silo.
    :return: Silo load visualization.
    :rtype: str
    """
    fill_cnt = int(Decimal(load / capacity * 10)
                   .quantize(Decimal(1), rounding=ROUND_HALF_UP))
    empty_cnt = 10 - fill_cnt
    return(f"[{"█" * fill_cnt}{"░" * empty_cnt}]")


def print_consolidated(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of items consolidated across silos.

    :param list[RocketSilo] silos: List of silos.
    :param int num_silos: Number of available silos.
    :return: None
    """
    print("\nConsolidated silo contents:")
    silo_index = 0
    while silo_index < num_silos:
        i = silo_index
        # Running list of silo items
        superlist: list[Item] = []
        while i < len(silos):
            superlist += silos[i].inventory
            i += num_silos
        total_weight = sum([float(x["weight"]) for x in superlist if x])
        rounded_weight = get_formatted_load(total_weight)
        print(f"\n\tSilo {silo_index + 1} ({rounded_weight} kg):")
        print_item_header()
        print_grouped_items(group_items(superlist))
        silo_index += 1


def print_grouped_items(items: dict[str, int]) -> None:
    """
    Prints the formatted name and count for each grouped item.

    Expects a dictionary of item names and counts.
    
    :param dict[str, int] items: Grouped item names and counts.
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


def group_items(items: list[Item]) -> dict[str, int]:
    """
    Consolidate and group together items by name, sorted by item id.

    :param list[Item] items: List of items.
    :return: Consolidated, sorted items and their counts.
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

    :param list[RocketSilo] silos: List of silos.
    :param int num_silos: Number of available silos.
    :return: Number of launch cycles.
    :rtype: int
    """
    return math.ceil(len(silos) / num_silos)
