class Container:
    def __init__(self, container, capacity):
        self.container = container
        self.capacity = capacity
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)
