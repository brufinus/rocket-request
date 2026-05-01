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
    "transportbelt": make_item("Transport belt", 100, 100),
    "chemicalplant": make_item("Chemical plant", 10, 10),
    "pipe": make_item("Pipe", 100, 200),
    "inserter": make_item("Inserter", 50, 50),
    "fasttransportbelt": make_item("Fast transport belt", 100, 100),
    "pipetoground": make_item("Pipe to ground", 50, 50),
    "undergroundbelt": make_item("Underground belt", 50, 50),
    "fastinserter": make_item("Fast inserter", 50, 50),
    "efficiencymodule": make_item("Efficiency module", 50, 50),
    "solarpanel": make_item("Solar panel", 50, 50),
    "crusher": make_item("Crusher", 10, 10),
    "assemblingmachine2": make_item("Assembling machine 2", 50, 50),
    "splitter": make_item("Splitter", 50, 50),
    "gunturret": make_item("Gun turret", 50, 50),
    "long-handedinserter": make_item("Long-handed inserter", 50, 50),
    "speedmodule": make_item("Speed module", 50, 50),
    "cargobay": make_item("Cargo bay", 10, 10),
    "foundry": make_item("Foundry", 20, 5),
    "rocketturret": make_item("Rocket turret", 10, 10),
    "fastundergroundbelt": make_item("Fast underground belt", 50, 50),
    "asteroidcollector": make_item("Asteroid collector", 10, 10),
    "steamturbine": make_item("Steam turbine", 10, 10),
    "thruster": make_item("Thruster", 10, 5),
    "speedmodule2": make_item("Speed module 2", 50, 50),
    "heatexchanger": make_item("Heat exchanger", 50, 25),
    "decidercombinator": make_item("Decider combinator", 50, 50),
    "bulkinserter": make_item("Bulk inserter", 50, 50),
    "beacon": make_item("Beacon", 20, 20),
    "nuclearreactor": make_item("Nuclear reactor", 10, 1)
}
