"""
Functions for requesting and validating user input.

Functions:
    request_silo_count: Request the number of available silos.
    parse_silo_count: Parses and validates the silo count.
    request_items: Request a list of items and their counts.
    search_item: Search for an item in the item data.
    is_done_adding_items: Checks whether the user is done adding items.
    get_similar_item: Get the most similar item key in the item data.
    transform_string: Transform a string to the expected key format.
"""

from difflib import SequenceMatcher
import re

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM, \
    ITEM_KEYWORDS, ITEM_NAME, ITEM_ROCKET_CAPACITY
from data.item import Item
from data.items import ITEMS


def request_silo_count() -> int:
    """
    Request the number rocket silos available to the user.

    :return: The number of available rocket silos.
    :rtype: int
    """
    while True:
        try:
            return parse_silo_count(input("Available rocket silos: "))
        except ValueError as e:
            print(e)


def parse_silo_count(raw_count: str) -> int:
    """
    Parses and validates silo count from a raw string.

    :param str raw_count: The silo count.
    :return: Parsed, validated silo count or -1 if invalid.
    :rtype: int
    :raises ValueError: If the value is not a positive integer.
    """
    try:
        num_silos = int(raw_count)
    except ValueError as e:
        raise ValueError(INPUT_INVALID_NUM) from e
    if num_silos <= 0:
        raise ValueError(INPUT_GREATER_ZERO)
    return num_silos


def request_items() -> list[tuple[str, int]]:
    """
    Request from the user a list of items and their counts.

    The user is prompted to enter an item to be inserted.
    If the item is valid, a count for the item is requested.
    The item and count are represented in a tuple.

    :return: The items to be inserted into the rocket silo(s).
    :rtype: list[tuple[str, int]]
    """
    print("Add items to the silo. Enter 'done' once finished.")
    items: list[tuple[str, int]] = []
    while True:
        user_input = input("Item: ")
        user_item = transform_string(user_input)
        if is_done_adding_items(user_item, items):
            break
        item = search_item(user_item, ITEMS)
        if item == "":
            similar_item = get_similar_item(user_item, ITEMS)
            if similar_item:
                if input(f"Did you mean '{
                    ITEMS[similar_item][ITEM_NAME]
                    }'? [y/n]: ").lower() == "y":
                    item = similar_item
        if item and ITEMS[item][ITEM_ROCKET_CAPACITY] > 0:
            while True:
                try:
                    count = int(input("Count: "))
                    if count > 0:
                        items.append((item, count))
                        break
                    print(INPUT_GREATER_ZERO)
                except ValueError:
                    print(INPUT_INVALID_NUM)
        else:
            print("Enter a valid item that can be inserted into "
                  "the rocket silo")

    return items


def is_done_adding_items(user_input: str,
                         items: list[tuple[str, int]]) -> bool:
    """
    Checks whether the user is done adding items.

    :param str input: The user input to check.
    :param list[tuple[str, int]] items: The list of items added so far.
    :return: Whether the user is done adding items.
    :rtype: bool
    """
    if user_input == "done":
        if not items:
            print("At least one item must be added to the silo.")
            return False
        return True
    return False


def search_item(item: str, item_data: dict[str, Item]) -> str:
    """
    Searches for the item in the given item data.

    First checks if the item is a key in the dictionary. If not, checks
    for the item in the keywords for each key in the dictionary.

    :param str search_item: The item to be searched for.
    :param dict[str, Item] item_data: The item data to check against.
    :return: The item key or an empty string.
    :rtype: str
    """
    if item in item_data:
        return item
    for k in item_data:
        if item in item_data[k].get(ITEM_KEYWORDS, []):
            return k
    return ""

def get_similar_item(item: str, item_data: dict[str, Item]) -> str:
    """
    Returns a key in the item data most similar to the given string.

    Returns an empty string if there is no match.

    :param str item: The item to compare similarity against.
    :param dict[str, Item] item_data: The item data to check against.
    :return: The most similar item key or an empty string.
    :rtype: str
    :var float threshold: The minimum ratio to be considered a match.
    """
    threshold: float = 0.6
    best_ratio = 0.0
    best_key = ""
    # If ratio is higher than confidence, immediately return the key.
    confidence: float = 0.85
    for k in item_data:
        similarity_ratio = SequenceMatcher(None, item, k).ratio()
        if similarity_ratio > confidence:
            return k
        if similarity_ratio > threshold and similarity_ratio > best_ratio:
            best_ratio = similarity_ratio
            best_key = k
    return best_key

def transform_string(raw_string: str) -> str:
    """
    Transforms the given string to the expected key format.

    Expected key format is the format of the keys in the item data.

    :param str raw_string: The string to be transformed.
    :return: The transformed string.
    :rtype: str
    """
    return re.sub(r"[ \-_]", "", raw_string).lower()
