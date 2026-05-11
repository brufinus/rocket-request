"""String constants"""

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
