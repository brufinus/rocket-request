from difflib import SequenceMatcher
import re

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
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
            num_silos = int(input("Available rocket silos: "))
            if num_silos > 0:
                return num_silos
            else:
                print(INPUT_GREATER_ZERO)
        except ValueError:
            print(INPUT_INVALID_NUM)


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
        if user_item.lower() == "done":
            if len(items) == 0:
                print("At least one item must be added to the silo.")
            else:
                break
        else:
            item = search_item(user_item, ITEMS)
            if item == "":
                similar_item = get_similar_item(user_item, ITEMS)
                if len(similar_item) > 0:
                    if input(f"Did you mean '{ITEMS[similar_item]["name"]}'? "
                             "[y/n]: ").lower() == "y":
                        item = similar_item
            if len(item) > 0 and ITEMS[item]["rocket_capacity"] > 0:
                while True:
                    try:
                        count = int(input("Count: "))
                        if count > 0:
                            items.append((item, count))
                            break
                        else:
                            print(INPUT_GREATER_ZERO)
                    except ValueError:
                        print(INPUT_INVALID_NUM)
            else:
                print("Enter a valid item that can be inserted into "
                      "the rocket silo")

    return items


def search_item(search_item: str, item_data: dict[str, Item]) -> str:
    """
    Searches for the item in the given item data.

    First checks if the item is a key in the dictionary. If not, checks
    for the item in the keywords for each key in the dictionary.

    :param str search_item: The item to be searched for.
    :param dict[str, Item] item_data: The item data to check against.
    :return: The item key or an empty string.
    :rtype: str
    """
    if search_item in item_data:
        return search_item
    for k in item_data:
        if search_item in item_data[k].get("keywords", []):
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
        elif similarity_ratio > threshold and similarity_ratio > best_ratio:
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
