def make_item(name, stack_size, rocket_capacity):
    """Return a dictionary of attributes with calculated weight."""
    return {
        "name": name,
        "stack_size": stack_size,
        "rocket_capacity": rocket_capacity,
        "weight": 1000 / rocket_capacity
    }


ITEMS = {
    "transport_belt": make_item("Transport belt", 100, 100),
    "chemical_plant": make_item("Chemical plant", 10, 10)
}
