import math

from models.containers.RocketSilo import RocketSilo


def print_distribution(silos: list[RocketSilo], num_silos: int) -> None:
    """
    Prints the distribution of items across available silos.

    :param silos: List of silos with items.
    :param num_silos: Number of available silos.
    :return: None
    """
    print(f"Total launches required: {len(silos)}")
    cycles = calculate_launch_cycles(silos, num_silos)
    print(f"Required launch cycles: {cycles}")

    silo_index = 0
    for i in range(cycles):
        print(f"Cycle {i + 1}:")
        for j in range(num_silos):
            print(f"\tSilo {j + 1}:")
            print(f"\t\tItem\tCount")
            # for item in silos[silo_index].inventory:
            print(silos[silo_index].inventory)


def condense_items(items: list[dict[str, str | int]]) -> dict[str, int]:
    """
    Condense items into name and item count.

    :param items: List of items in the silo.
    :return: Condensed list of each item and their count.
    :rtype: dict
    """
    condensed_items: dict[str, int] = {}
    for item in items:
        condensed_items.update(
            {str(item["name"]): condensed_items.get(str(item["name"]), 0) + 1})
    return condensed_items


def calculate_launch_cycles(silos: list[RocketSilo], num_silos: int) -> int:
    """
    Calculates the number launch cycles required.

    :param silos: List of silos with items.
    :param num_silos: Number of available silos.
    :return: Number of launch cycles.
    :rtype: int
    """
    return math.ceil(len(silos) / num_silos)
