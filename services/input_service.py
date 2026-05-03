from difflib import SequenceMatcher

from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from data.items import ITEMS


def request_silo_count() -> int:
    """
    Request from the user the number of available rocket silos.

    :return: The number of available rocket silos.
    :rtype: int
    """
    while True:
        try:
            num_silos = int(input("Number of Rocket silos: "))
            if num_silos > 0:
                return num_silos
            else:
                print(INPUT_GREATER_ZERO)
        except ValueError:
            print(INPUT_INVALID_NUM)


def request_items() -> list[tuple[str, int]]:
    """
    Request from the user a list of items and their
    count to be inserted into the rocket silo(s).
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
            item = validate_item(user_item, ITEMS)
            if item == "":
                similar_item = get_similar_item(user_item, ITEMS)
                if len(similar_item) > 0:
                    if input(f"Did you mean '{ITEMS[similar_item]["name"]}'? "
                             "[y/n]: ").lower() == "y":
                        item = similar_item
            if len(item) > 0:
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


def validate_item(item: str,
                  dictionary: dict[str, dict[str, str | float | list[str]]]) \
                    -> str:
    """
    Validates whether the item is in the given
    dictionary and returns the key if it is.

    :param item: The item to be validated.
    :param dictionary: The dictionary to check against.
    :return: The item key or an empty string.
    :rtype: str
    """
    if item in dictionary:
        return item
    for k in dictionary:
        if item in dictionary[k]["keywords"]:
            return k
    return ""

def get_similar_item(item: str, dictionary: 
                      dict[str, dict[str, str | float | list[str]]]) -> str:
    """
    Returns the key from a dictionary most similar to the given string.
    Returns an empty string if there is no match.

    :param item: The item to compare similarity against.
    :param dictionary: The dictionary to check against.
    :return: The most similar item key or an empty string.
    :rtype: str
    """
    best_ratio = 0.0
    best_key = ""
    # If ratio is higher than confidence, immediately return the key.
    confidence: float = 0.85
    for k in dictionary:
        similarity_ratio = SequenceMatcher(None, item, k).ratio()
        if similarity_ratio > confidence:
            return k
        elif similarity_ratio > 0.6 and similarity_ratio > best_ratio:
            best_ratio = similarity_ratio
            best_key = k
    return best_key

def transform_string(string: str) -> str:
    """
    Transforms the given string to the expected key format.

    :param string: The string to be transformed.
    :return: The transformed string.
    :rtype: str
    """
    return string.lower().replace(" ", "").replace("-", "").replace("_", "")
