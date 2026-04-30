from data.items import ITEMS
from models.containers.RocketSilo import RocketSilo


def distribute_items(num_silos: int, items: list[tuple[str, int]]) -> None:
    """
    Distribute items into silos.

    :param num_silos: Maximum number of silos.
    :param items: List of items to distribute amongst silos.
    :return: None
    """
    # items = [("item1", 10), ("item2", 5)...]
    expanded_items = []
    for item in items:
        for i in range(0, item[1]):
            expanded_items.append(ITEMS[item[0]])

    # Order items from heaviest to lightest.
    expanded_items.sort(reverse=True, key=lambda d: d['weight'])

    # Open a new empty silo.
    silos = [RocketSilo()]
    
    # For each item, find the first silo into which it can fit.
    for item in expanded_items:
        for silo in silos:
            if silo.add_item(item):
                break
            else:
                new_silo = RocketSilo()
                new_silo.add_item(item)
                silos.append(new_silo)



    print(expanded_items)
