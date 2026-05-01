def make_item(name: str, stack_size: int, rocket_capacity: int,
              keywords: list[str] = None) -> dict[str, str | int | list[str]]:
    """
    Return a dictionary of attributes with calculated weight.

    :return: Dictionary of an item's attributes.
    :rtype: dict[str, str | int]
    """
    return {
        "name": name,
        "stack_size": stack_size,
        "rocket_capacity": rocket_capacity,
        "weight": int(1000 / rocket_capacity),
        "keywords": keywords or []
    }


ITEMS = {
    "transportbelt": make_item("Transport belt", 100, 100, ["belt"]),
    "chemicalplant": make_item("Chemical plant", 10, 10, ["chemplant"])
}
