from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from data.items import ITEMS


def request_silo_count():
    while True:
        try:
            num_silos = int(input("Number of Rocket silos: "))
            if num_silos > 0:
                return num_silos
            else:
                print(INPUT_GREATER_ZERO)
        except ValueError:
            print(INPUT_INVALID_NUM)


def request_items():
    print("Add items to the silo. Enter 'done' once finished.")
    items = []
    while True:
        user_item = input("Item: ")
        if user_item.lower() == "done":
            if len(items) == 0:
                print("At least one item must be added to the silo.")
            else:
                break
        else:
            item = get_item(user_item)
            if len(item) > 0:
                while True:
                    try:
                        count = int(input("Count: "))
                        if count > 0:
                            items.append((item, count))
                            break
                        else:
                            print(INPUT_GREATER_ZERO)
                    except ValueError:
                        print(INPUT_INVALID_NUM)
            else:
                print("Invalid item. Enter an item that can be inserted into "
                      "the rocket silo")

    return items


def get_item(item):
    transformed_item = item.lower().replace(" ", "_")
    if transformed_item in ITEMS:
        return transformed_item
    return ""
