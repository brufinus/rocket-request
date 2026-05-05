"""
Service for requesting user input.

Functions:
    request_silo_count: Request the number of available silos.
    request_items: Request a list of items and their counts.
    confirm_suggested_item: Confirms a suggested item.
    is_done_adding_items: Checks whether the user is done adding items.
"""

from data.constants import ITEM_NAME
from data.items import ITEMS
from services.helper import transform_string
from services.search import search_coordinator
from services.validation import is_insertable, parse_count


def request_silo_count() -> int:
    """
    Request the number rocket silos available to the user.

    :return: The number of available rocket silos.
    :rtype: int
    """
    while True:
        try:
            return parse_count(input("Available rocket silos: "))
        except ValueError as e:
            print(e)


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

        search_res = search_coordinator(user_item, ITEMS)
        item = ""
        if search_res[0]:
            if search_res[1]:
                item = confirm_suggested_item(
                    input(f"Did you mean '{ITEMS[search_res[0]][ITEM_NAME]}'? [y/n]: "),
                    search_res[0],
                )
            else:
                item = search_res[0]

        if is_insertable(item, ITEMS):
            while True:
                try:
                    count = parse_count(input("Count: "))
                    items.append((item, count))
                    break
                except ValueError as e:
                    print(e)
        else:
            print("Enter a valid item that can be inserted into the rocket silo")

    return items


def confirm_suggested_item(input_str: str, item: str) -> str:
    """
    Confirms whether to accept the suggested item.

    :param str input_str: The user input.
    :param str item: The suggested item.
    :return: The accepted suggestion or an empty string.
    :rtype: str
    """
    if transform_string(input_str) == "y":
        return item
    return ""


def is_done_adding_items(user_input: str, items: list[tuple[str, int]]) -> bool:
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
