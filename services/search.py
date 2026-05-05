"""
Search service for rocket silo.

Functions
    search_coordinator: Coordinates item searching service.
    search_item: Search for an item in the item data.
    search_similar_item: Get the most similar item in the item data.
"""

from difflib import SequenceMatcher

from data.constants import ITEM_KEYWORDS
from data.item import Item


def search_coordinator(
    search_string: str, item_data: dict[str, Item]
) -> tuple[str, bool]:
    """
    Coordinates the search of a string in the given item data.

    First searches for the search string as a key or keyword,
    then searches for similar results.

    :param str search_string: The string to search for.
    :param dict[str, Item]: The item data.
    :return: A found key or nothing, and whether the result is a
    suggestion or not.
    :rtype: tuple[str, bool]
    """
    search_res = search_item(search_string, item_data)
    if search_res:
        return (search_res, False)
    search_res = search_similar_item(search_string, item_data)
    if search_res:
        return (search_res, True)
    return ("", False)


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


def search_similar_item(item: str, item_data: dict[str, Item]) -> str:
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
