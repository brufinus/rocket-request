def make_item(name: str, stack_size: int, rocket_capacity: int) -> dict[
    str, str | int]:
    """
    Return a dictionary of attributes with calculated weight.

    :return: Dictionary of an item's attributes.
    :rtype: dict[str, str | int]
    """
    return {
        "name": name,
        "stack_size": stack_size,
        "rocket_capacity": rocket_capacity,
        "weight": int(1000 / rocket_capacity)
    }


ITEMS = {
    "transport_belt": make_item("Transport belt", 100, 100),
    "chemical_plant": make_item("Chemical plant", 10, 10)
}
