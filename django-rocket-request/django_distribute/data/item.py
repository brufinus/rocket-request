"""
Defines the Item TypedDict, which represents the structure of an item.

Classes:
    Item: A TypedDict that defines the attributes of an item.
"""

from typing import NotRequired, Required, TypedDict


class Item(TypedDict):
    """
    Defines the attributes of the item dict.
    
    Attributes:
        name (str): The official name of the item.
        stack_size (int): The item's maximum stack size.
        rocket_capacity (int): The number of items one silo can hold.
        weight (float): The weight of the item.
        id (int): The unique identifier for the item.
        keywords (list[str]): A list of potential keywords.
    """
    name: Required[str]
    stack_size: Required[int]
    rocket_capacity: Required[int]
    weight: Required[float]
    id: Required[int]
    keywords: NotRequired[list[str]]
