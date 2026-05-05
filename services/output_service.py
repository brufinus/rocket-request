"""
Service for outputting data from the program.

Functions:
    get_load_visualization: Returns a visualization of the silo load.
    print_consolidated: Prints items consolidated across silos.
    print_cycle_header: Prints cycle header separator.
    print_distribution: Prints the distribution of items across silos.
    print_distribution_info: Prints distribution logistic info.
    print_grouped_items: Prints formatted name and count for each item.
    print_item_header: Prints the Item, Count header.
    print_silo_header: Prints silo header information.
"""

from decimal import ROUND_HALF_UP, Decimal
import math

from models.containers.rocketsilo import RocketSilo
from services.helper import get_col_width, get_formatted_float
from services.initialize_setup import (
    build_consolidated_invs,
    build_consolidated_load,
    build_distribution,
)


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
        load, capacity)} ({get_formatted_float(load)}/{capacity} kg):")


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
