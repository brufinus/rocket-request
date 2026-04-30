from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo


def distribute_items(num_silos: int, items: list[tuple[str, int]]) -> None:
    """
    Distribute items into silos.

    :param num_silos: Maximum number of silos.
    :param items: List of items to distribute amongst silos.
    :return: None
    """
    expanded_items = expand_and_sort_items(items)
    silos = [RocketSilo()]
    first_fit_silo(silos, expanded_items)

    print(expanded_items)


def first_fit_silo(silos: list[RocketSilo],
                   items: list[dict[str, str | int]]) -> None:
    """
    First-fit-decreasing algorithm to distribute items into silos.
    For each item, find the first silo into which it can fit.
    If it did not fit into any silo, open a new one and add it.

    :param silos: List of silos to search through.
    :param items: List of items to distribute.
    :return: None
    """
    for item in items:
        if not find_open_silo(silos, item):
            new_silo = RocketSilo()
            new_silo.add_item(item)
            silos.append(new_silo)


def find_open_silo(silos: list[RocketSilo],
                   item: dict[str, str | int]) -> bool:
    """
    Find the first silo into which the item can fit.

    :param silos: List of silos to search through.
    :param item: Item to add to a silo.
    :return: Whether the item was added to a silo.
    :rtype: bool
    """
    for silo in silos:
        if silo.add_item(item):
            return True
    return False


def expand_and_sort_items(
        items: list[tuple[str, int]]) -> list[dict[str, str | int]]:
    """
    Expand items into a sorted list of item dictionaries.
    Items are sorted from heaviest to lightest.

    :param items: List of items to expand.
    :return: Expanded list of item dictionaries.
    :rtype: list[dict[str, str | int]]
    """
    expanded_items: list[dict[str, str | int]] = []
    for item in items:
        for _ in range(item[1]):
            expanded_items.append(ITEMS[item[0]])
    expanded_items.sort(reverse=True, key=lambda d: d['weight'])
    return expanded_items
