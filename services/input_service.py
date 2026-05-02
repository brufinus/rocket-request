from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM
from data.items import ITEMS


def request_silo_count() -> int:
    """
    Request from the user the number of available rocket silos.

    :return: The number of available rocket silos.
    :rtype: int
    """
    while True:
        try:
            num_silos = int(input("Number of Rocket silos: "))
            if num_silos > 0:
                return num_silos
            else:
                print(INPUT_GREATER_ZERO)
        except ValueError:
            print(INPUT_INVALID_NUM)


def request_items() -> list[tuple[str, int]]:
    """
    Request from the user a list of items and item count to be inserted into
    the rocket silo(s). The item and count are represented in a tuple.

    :return: The items and count to be inserted into the rocket silo(s).
    :rtype: list[tuple[str, int]]
    """
    print("Add items to the silo. Enter 'done' once finished.")
    items: list[tuple[str, int]] = []
    while True:
        user_input = input("Item: ")
        user_item = transform_string(user_input)
        if user_item.lower() == "done":
            if len(items) == 0:
                print("At least one item must be added to the silo.")
            else:
                break
        else:
            item = validate_item(user_item, ITEMS)
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


def validate_item(item: str, dictionary: dict[str, dict[str, str | int | list[str]]]) -> str:
    """
    Validates whether the item is in the given
    dictionary and returns the key if it is.

    :param item: The item to be validated.
    :return: The item key or an empty string.
    :rtype: str
    """
    if item in dictionary:
        return item

    for k in dictionary:
        if item in str(dictionary[k]["keywords"]):
            return k

def transform_string(string: str) -> str:
    """
    Transforms the given string to the expected key format.

    :param string: The string to be transformed.
    :return: The transformed string.
    :rtype: str
    """
    return string.lower().replace(" ", "").replace("-", "").replace("_", "")
