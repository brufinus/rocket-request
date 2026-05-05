"""
Initializes and prints the setup for item distribution across silos.

Functions:
    print_distribution: Prints the distribution of items across silos.
    build_distribution: Builds silo item distribution data.
    print_distribution_info: Prints distribution logistic info.
    print_cycle_header: Prints cycle header separator.
    print_silo_header: Prints silo header information.
    get_formatted_load: Formats the load to a string.
    get_load_visualization: Returns a visualization of the silo load.
    print_consolidated: Prints items consolidated across silos.
    build_consolidated_invs: Builds consolidated inventory data.
    build_consolidated_loads: Builds consolidated weight data.
    get_consolidated_slots: Consolidates slots across cycles.
    print_grouped_items: Prints formatted name and count for each item.
    print_item_header: Prints the Item, Count header.
    get_col_width: Returns a column width for output padding.
    group_items: Consolidates and groups items together.
    calculate_launch_cycles: Calculates the number of launch cycles.
"""

from decimal import ROUND_HALF_UP, Decimal
import math

from data.constants import ITEM_ID, ITEM_NAME
from data.item import Item
from data.items import ITEMS
from models.containers.rocketsilo import RocketSilo


def print_distribution(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of items across available silos.

    :param list[RocketSilo] silos: List of silos with distributed items.
    :param int num_silos: The number of silos available to the user.
    :return: None
    """
    cycles = build_distribution(silos, num_silos)
    num_cycles = len(cycles)
    print_distribution_info(len(silos), num_cycles)

    # Keeps track of the current silo across all cycles.
    silo_index = 0
    for cycle_index, cycle in enumerate(cycles):
        print_cycle_header(cycle_index + 1, num_cycles)
        for inv_index, silo_inv in enumerate(cycle):
            print_silo_header(
                inv_index + 1, silos[silo_index].load, RocketSilo.CAPACITY
            )
            print_item_header()
            print_grouped_items(silo_inv)
            silo_index += 1


def print_distribution_info(num_launches: int, num_cycles: int) -> None:
    """
    Prints information about the distribution logistics.

    The number of launches is equivalent
    to the number of available silos.

    :param int num_launches: Total number of required launches.
    :param int num_cycles: Total number of required cycles.
    :return: None
    """
    print(f"\nTotal launches required: {num_launches}")
    print(f"Required launch cycles: {num_cycles}")


def print_cycle_header(current_cycle: int, num_cycles: int) -> None:
    """
    Prints a cycle header to separate cycles.

    :param int current_cycle: The current cycle number.
    :param int num_cycles: The total number of cycles.
    :return: None
    """
    # Calculates total extra digits and adds that many separators.
    separators = "═" * int(math.log10(current_cycle) + math.log10(num_cycles) + 1)
    print(f"╔═══════════════════════{separators}╗")
    print(f"║      Cycle {current_cycle} of {num_cycles}      ║")
    print(f"╚═══════════════════════{separators}╝")


def print_silo_header(silo_num: int, load: float, capacity: int) -> None:
    """
    Prints a silo information header with the given inputs.

    Intended to be printed for each silo in a cycle.

    :param int silo_num: The current silo number in a cycle.
    :param float load: The load of the silo in a cycle.
    :param int capacity: The capacity of a silo.
    :return: None
    """
    print(f"\n\tSilo {silo_num} {get_load_visualization(
        load, capacity)} ({get_formatted_load(load)}/{capacity} kg):")


def build_distribution(
    silos: list[RocketSilo], num_silos: int
) -> list[list[dict[str, int]]]:
    """
    Builds data of silo item distribution across cycles.

    Groups silos per cycle, grouping items within each silo, and
    returns a list of cycles containing a list of silo inventories.

    :param list[RocketSilo] silos: List of silos with distributed items.
    :param int num_silos: The number of silos available to the user.
    :return: A list of silo inventories in each cycle.
    :rtype: list[list[dict[str, int]]]
    """
    num_cycles = calculate_launch_cycles(silos, num_silos)
    cycles = []
    silo_index = 0
    for _ in range(num_cycles):
        cycle = []
        for _ in range(num_silos):
            if silo_index >= len(silos):
                break
            cycle.append(group_items(silos[silo_index].inventory))
            silo_index += 1
        cycles.append(cycle)
    return cycles


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
    return f"{load:.1f}"


def get_load_visualization(load: float, capacity: int) -> str:
    """
    Returns a visualization of the silo load in progress bar format.

    Example: [█████░░░░░] for 50% load.

    :param float load: The current load of the silo.
    :param int capacity: The maximum capacity of the silo.
    :return: Silo load visualization.
    :rtype: str
    """
    fill_cnt = int(
        Decimal(load / capacity * 10).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    )
    empty_cnt = 10 - fill_cnt
    return f"[{"█" * fill_cnt}{"░" * empty_cnt}]"


def print_consolidated(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of silo inventories consolidated across cycles.

    :param list[RocketSilo] silos: List of silos.
    :param int num_silos: Number of available silos.
    :return: None
    """
    print("\nConsolidated silo contents:")
    c_silo_invs = build_consolidated_invs(silos, num_silos)
    c_silo_loads = build_consolidated_load(silos, num_silos)
    for inv_index, inv in enumerate(c_silo_invs):
        print(f"\n\tSilo {inv_index + 1} ({c_silo_loads[inv_index]} kg):")
        print_item_header()
        print_grouped_items(inv)


def build_consolidated_load(silos: list[RocketSilo], num_silos: int) -> list[str]:
    """
    Builds data of silo load, consolidated across cycles.

    Consolidates the load of each silo slot, which is limited by
    the number of physically available silos, across cycles.

    :param list[RocketSilo] silos: List of silos with distributed items.
    :param int num_silos: The number of silos available to the user.
    :return: A consolidated list of silo loads in each cycle.
    :rtype: list[str]
    """
    slots = get_consolidated_slots(silos, num_silos)
    consolidated_weights: list[str] = []
    for slot in slots:
        superweight = 0.0
        for silo in slot:
            superweight += silo.load
        consolidated_weights.append(get_formatted_load(superweight))
    return consolidated_weights


def build_consolidated_invs(
    silos: list[RocketSilo], num_silos: int
) -> list[dict[str, int]]:
    """
    Builds data of silo item distribution, consolidated across cycles.

    Consolidates the inventory of each silo slot, which is limited by
    the number of physically available silos, across cycles.

    :param list[RocketSilo] silos: List of silos with distributed items.
    :param int num_silos: The number of silos available to the user.
    :return: A consolidated list of silo inventories in each cycle.
    :rtype: list[dict[str, int]]
    """
    slots = get_consolidated_slots(silos, num_silos)
    consolidated_invs: list[dict[str, int]] = []
    for slot in slots:
        superlist = []
        for silo in slot:
            superlist += silo.inventory
        consolidated_invs.append(group_items(superlist))
    return consolidated_invs


def get_consolidated_slots(
    silos: list[RocketSilo], num_silos: int
) -> list[list[RocketSilo]]:
    """
    Consolidates the slots of each physical silo across cycles.

    :param list[RocketSilo] silos: List of silos with distributed items.
    :param int num_silos:
    The number physical silos available to the user.
    :return: A list of consolidated silo slots across cycles.
    :rtype: list[list[RocketSilo]]
    """
    consolidated_slots: list[list[RocketSilo]] = []
    silo_index = 0
    # Loop through physical silos.
    while silo_index < num_silos:
        # Running list of silos.
        superlist: list[RocketSilo] = []
        i = silo_index
        # Loop through silo slots across cycles.
        while i < len(silos):
            superlist.append(silos[i])
            i += num_silos
        consolidated_slots.append(superlist)
        silo_index += 1
    return consolidated_slots


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
    Consolidates and groups together items by name, sorted by item id.

    :param list[Item] items: List of items.
    :return: Consolidated, sorted items and their counts.
    :rtype: dict[str, int]
    """
    grouped_items: dict[str, int] = {}
    uids = []
    for item in items:
        uids.append(item[ITEM_ID])
    uids.sort()
    for uid in uids:
        # Get item name using id.
        name = str([x[ITEM_NAME] for x in items if uid == x[ITEM_ID]][0])
        # Set item or increment its count.
        grouped_items.update({name: grouped_items.get(name, 0) + 1})
    return grouped_items


def calculate_launch_cycles(silos: list[RocketSilo], num_silos: int) -> int:
    """
    Calculates the number of launch cycles required.

    :param list[RocketSilo] silos: List of silos.
    :param int num_silos: Number of available silos.
    :return: Number of launch cycles.
    :rtype: int
    """
    return math.ceil(len(silos) / num_silos)
