"""
Initializes the setup of distributed items.

Functions:
    build_distribution: Builds silo item distribution data.
    build_consolidated_invs: Builds consolidated inventory data.
    build_consolidated_loads: Builds consolidated weight data.
    get_consolidated_slots: Consolidates slots across cycles.
    group_items: Consolidates and groups items together.
    calculate_launch_cycles: Calculates the number of launch cycles.
"""

import math

from data.constants import ITEM_ID, ITEM_NAME
from data.item import Item
from models.containers.rocketsilo import RocketSilo
from services.helper import get_formatted_float


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
        consolidated_weights.append(get_formatted_float(superweight))
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
