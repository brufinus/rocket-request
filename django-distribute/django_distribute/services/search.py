"""
Search service for rocket silo.

Functions
    search_coordinator: Coordinates item searching service.
    search_item: Search for an item in the item data.
    search_similar_item: Get the most similar item in the item data.
"""

from difflib import SequenceMatcher

from django_distribute.data.constants import ITEM_KEYWORDS
from django_distribute.models import Item
from django_distribute.services.helper import transform_string


def search_coordinator(search_string: str) -> tuple[str, bool]:
    """
    Coordinates the search of an item in the Item data.

    First searches for the search string as a key or keyword,
    then searches for similar results.

    :param str search_string: The string to search for.
    :return: A found key or nothing, and whether the result is a
    suggestion or not.
    :rtype: tuple[str, bool]
    """
    search_res = search_item(search_string)
    if search_res:
        return (search_res, False)
    search_res = search_similar_item(search_string)
    if search_res:
        return (search_res, True)
    return ("", False)


def search_item(item: str) -> str:
    """
    Searches for the item in the Item data.

    First checks if the item is a key in the dictionary. If not, checks
    for the item in the keywords for each key in the dictionary.

    :param str search_item: The item to be searched for.
    :return: The item key or an empty string.
    :rtype: str
    """
    try:
        return str(Item.objects.get(name__iexact=item))
    except Item.DoesNotExist:
        item = transform_string(item)
        try:
            return str(Item.objects.get(name_slug__iexact=item))
        except Item.DoesNotExist:
            try:
                return str(Item.objects.get(keywords__keyword=item))
            except Item.DoesNotExist:
                return ""


def search_similar_item(item: str) -> str:
    """
    Returns a key in the Item data most similar to the given string.

    Returns an empty string if there is no match.

    :param str item: The item to compare similarity against.
    :return: The most similar item key or an empty string.
    :rtype: str
    :var float threshold: The minimum ratio to be considered a match.
    """
    threshold: float = 0.6
    best_ratio = 0.0
    best_key = ""
    # If ratio is higher than confidence, immediately return the key.
    confidence: float = 0.85
    for k in Item.objects.all():
        similarity_ratio = SequenceMatcher(None, item, str(k)).ratio()
        if similarity_ratio > confidence:
            return str(k)
        if similarity_ratio >= threshold and similarity_ratio > best_ratio:
            best_ratio = similarity_ratio
            best_key = k
    return str(best_key)
