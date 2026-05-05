"""
Services for validating input.

Functions:
    parse_count: Parses and validates count.
    is_insertable: Checks whether a single item can be inserted.
"""

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM, ITEM_ROCKET_CAPACITY
from data.item import Item


def parse_count(raw_count: str) -> int:
    """
    Parses and validates count from a raw string.

    :param str raw_count: The raw count.
    :return: The parsed and validated count.
    :rtype: int
    :raises ValueError: If the value is not a positive integer.
    """
    try:
        count = int(raw_count)
    except ValueError as e:
        raise ValueError(INPUT_INVALID_NUM) from e
    if count <= 0:
        raise ValueError(INPUT_GREATER_ZERO)
    return count


def is_insertable(item: str, item_data: dict[str, Item]) -> bool:
    """
    Checks whether an item can be inserted into a silo.

    This function only checks if a single item's rocket capacity is
    too large for a silo. It does not check the item weight against a
    silo's load.

    :param str item: The item to validate.
    :param dict[str, Item]: The item database.
    :return: Whether the item is insertable.
    :rtype: bool
    """
    if item and item_data[item][ITEM_ROCKET_CAPACITY] > 0:
        return True
    return False
