"""
Distribution service for the rocket silo program.

This module contains the logic for distributing items into silos.

Functions:
    distribute_items: Coordinates distribution of items into silos.
    first_fit_silo: Distributes items into silos using first-fit.
    find_open_silo: Tries to add an item into the first open silo.
    expand_and_sort_items: Expands items into a sorted list of items.
"""

from django_distribute.containers.rocketsilo import RocketSilo
from django_distribute.data.constants import ITEM_WEIGHT
from django_distribute.data.item import Item
from django_distribute.data.items import ITEMS


def distribute_items(items: dict[str, int]) -> list[RocketSilo]:
    """
    Coordinates the distribution of items into silos.

    Items are first expanded into individual units and sorted.
    Then, a first-fit-decreasing algorithm is used to distribute items
    into RocketSilos.

    :param dict[str, int] items:
    Item name and count pairs to distribute.
    :return: List of silos with distributed items.
    :rtype: list[RocketSilo]
    """
    expanded_items = expand_and_sort_items(items)
    silos = [RocketSilo()]
    for item in expanded_items:
        first_fit_silo(silos, item)
    return silos


def first_fit_silo(silos: list[RocketSilo], item: Item) -> None:
    """
    Runs a first-fit algorithm to insert the item into a silo.

    Tries to add the item into the first silo with enough space.
    If there are no open silos, it is added to a new one.

    :param list[RocketSilo] silos: List of silos to search through.
    :param Item item: The item to add.
    :return: None
    """
    for silo in silos:
        if silo.load < RocketSilo.CAPACITY and silo.add_item(item):
            return
    new_silo = RocketSilo()
    new_silo.add_item(item)
    silos.append(new_silo)


def expand_and_sort_items(items: dict[str, int]) -> list[Item]:
    """
    Expands items into a sorted list of items.

    Expansion involves adding each item to a list as many times as its
    count, which are both provided as a tuple pair in the input list.
    Items are are then sorted from heaviest to lightest.

    :param dict[str, int] items:
    Item name and count pairs to distribute.
    :return: Expanded list of items.
    :rtype: list[Item]
    """
    expanded_items: list[Item] = []
    for item in items:
        for _ in range(items[item]):
            expanded_items.append(ITEMS[item])
    expanded_items.sort(reverse=True, key=lambda d: d[ITEM_WEIGHT])
    return expanded_items
