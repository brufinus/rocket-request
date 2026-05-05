"""
Helper functions for services.

Functions:
    get_col_width: Returns a column width for output padding.
    get_formatted_float: Formats a float to a string.
    transform_string: Transform a string to the expected key format.
"""


import re

from data.items import ITEMS


def get_formatted_float(raw_float: float) -> str:
    """
    Formats the given float to a string.

    This method rounds the float to the first decimal place
    or to the whole number if there are no decimals.

    :param float raw_float: The float to format.
    :return: The formatted float.
    :rtype: str
    """
    if raw_float % 1 == 0:
        return f"{int(raw_float)}"
    return f"{raw_float:.1f}"


def get_col_width() -> int:
    """
    Returns a column width for output padding.

    Determined using the longest key from item data.
    
    :param dict[str, Item] item_data: The item data to use.
    :return: The column width.
    :rtype: int
    """
    return len(max(ITEMS, key=len)) + 2


def transform_string(raw_string: str) -> str:
    """
    Transforms the given string to the expected key format.

    Expected key format is the format of the keys in the item data.

    :param str raw_string: The string to be transformed.
    :return: The transformed string.
    :rtype: str
    """
    return re.sub(r"[ \-_]", "", raw_string).lower()
