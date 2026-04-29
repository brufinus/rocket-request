from data.items import ITEMS


def setup():
    while True:
        try:
            num_silos = int(input("Number of Rocket silos: "))
            if num_silos > 0:
                break
            else:
                print("Enter a value greater than zero.")
        except ValueError:
            print("Invalid input. Enter a number greater than zero.")
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
                            print("Enter a value greater than zero.")
                    except ValueError:
                        print("Invalid input. Enter a number greater than zero.")
            else:
                print("Invalid item. Enter an item that can be inserted into the rocket silo.")

    return items

def get_item(item):
    transformed_item = item.lower().replace(" ", "_")
    if transformed_item in ITEMS:
        return transformed_item
    return ""
