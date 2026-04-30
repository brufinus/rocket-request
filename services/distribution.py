from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo


def distribute_items(num_silos, items) -> None:
    # items = [("item1", 10), ("item2", 5)...]
    expanded_items = []
    for item in items:
        for i in range(0, item[1]):
            expanded_items.append(ITEMS[item[0]])

    expanded_items.sort(reverse=True, key=lambda d: d['weight'])

    silos = [RocketSilo()]
    # for silo in silos:

    print(expanded_items)
