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
        item = input("Item: ")
        if item.lower() == "done":
            if len(items) == 0:
                print("At least one item must be added to the silo.")
            else:
                break
        else:
            # TODO: Validate the item.
            if len(items) > 0:
                while True:
                    try:
                        count = int(input("Count: "))
                        if count > 0:
                            break
                        else:
                            print("Enter a value greater than zero.")
                    except ValueError:
                        print("Invalid input. Enter a number greater than zero.")

    return items

# def is_valid_item(item):
