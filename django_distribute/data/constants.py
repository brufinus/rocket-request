"""String constants"""

# pylint: disable=line-too-long

from enum import StrEnum

# Error messages
INPUT_GREATER_ZERO = "Enter a value greater than zero."
INPUT_INVALID_NUM = f"Invalid input. {INPUT_GREATER_ZERO}"

# Item attributes
ITEM_STACK = "stack_size"
ITEM_ROCKET_CAPACITY = "rocket_capacity"
ITEM_WEIGHT = "weight"
ITEM_ID = "id"
ITEM_KEYWORDS = "keywords"


class Errors(StrEnum):
    """Error messages."""

    NO_ITEMS_ADDED = "No items have been added."
    ADD_ITEMS_DISTRIBUTE = "Please add items to distribute."
    IMPORT_ERROR = "Import failed due to invalid blueprint string."
    INVALID_ITEM = "Blueprint contains invalid item: "
    ITEMS_EXCEED_SLOTS = "Unable to create a valid blueprint as the number of items exceeds the number of chest slots."
