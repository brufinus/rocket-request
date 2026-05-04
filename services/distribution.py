"""
Distribution service for the rocket silo program.

This module contains the logic for distributing items into silos.

Functions:
    distribute_items: Distributes items into silos.
    first_fit_silo: Distributes items into silos using first-fit.
    find_open_silo: Tries to add an item into the first open silo.
    expand_and_sort_items: Expands items into a sorted list of items.
"""

from data.constants import ITEM_WEIGHT
from data.item import Item
from data.items import ITEMS
from models.containers.rocketsilo import RocketSilo


def distribute_items(items: list[tuple[str, int]]) -> list[RocketSilo]:
    """
    Distributes items into silos.

    :param list[tuple[str, int]] items:
    List of item, count pairs to distribute amongst silos.
    :return: List of silos with distributed items.
    :rtype: list[RocketSilo]
    """
    expanded_items = expand_and_sort_items(items)
    silos = [RocketSilo()]
    first_fit_silo(silos, expanded_items)
    return silos


def first_fit_silo(silos: list[RocketSilo], items: list[Item]) -> None:
    """
    Distributes items into silos using a first-fit algorithm.

    First-fit-decreasing:
    For each item, it finds the first silo into which it can fit.
    If it did not fit into any silo, a new one
    is created and the item is added to it.

    :param list[RocketSilo] silos: List of silos to search through.
    :param list[Item] items: List of items to distribute.
    :return: None
    """
    for item in items:
        if not find_open_silo(silos, item):
            new_silo = RocketSilo()
            new_silo.add_item(item)
            silos.append(new_silo)


def find_open_silo(silos: list[RocketSilo], item: Item) -> bool:
    """
    Tries to add the item into the first silo with enough space.

    :param list[RocketSilo] silos: List of silos to search through.
    :param Item item: The item to add.
    :return: Whether the item was added to a silo.
    :rtype: bool
    """
    for silo in silos:
        if silo.add_item(item):
            return True
    return False


def expand_and_sort_items(items: list[tuple[str, int]]) -> list[Item]:
    """
    Expands items into a sorted list of items.

    Expansion involves adding each item to a list as many times as its
    count, which are both provided as a tuple pair in the input list.
    Items are are then sorted from heaviest to lightest.

    :param list[tuple[str, int]] items:
    List of item, count pairs to expand.
    :return: Expanded list of items.
    :rtype: list[Item]
    """
    expanded_items: list[Item] = []
    for item in items:
        for _ in range(item[1]):
            expanded_items.append(ITEMS[item[0]])
    expanded_items.sort(reverse=True, key=lambda d: d[ITEM_WEIGHT])
    return expanded_items
