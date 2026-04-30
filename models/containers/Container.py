class Container:
    """
    Abstract base class for containers.

    Attributes:
        container (str): The name of the container.
        capacity (int): The maximum amount the container can have.
        inventory (list): A list of items in the container.
        load (int): The current load of the container.
    """

    def __init__(self, container, capacity) -> None:
        self.container = container
        self.capacity = capacity
        self.inventory = []
        self.load = 0

    def add_item(self, item) -> bool:
        """
        Adds an item to the container.

        :param dict item: The item to add.
        :return: True if the item was added, False otherwise.
        :rtype: bool
        """
        if self.can_add_item(item):
            self.inventory.append(item)
            self.increase_load(item)
            return True
        return False

    def can_add_item(self, item) -> bool:
        """
        Checks if the container has enough space to add an item.

        :param dict item: The item to check.
        :return: True if the container has enough space to add an item,
        False otherwise.
        :rtype: bool
        """
        if self.load + 1 < self.capacity:
            return True
        return False

    def increase_load(self, item) -> None:
        """
        Increases the current load of the container using the given item.

        :param dict item: The item to increase load with.
        :return: None
        """
        self.load += 1

    def remove_item(self, item) -> None:
        """
        Removes an item from the container.

        :param dict item: The item to remove.
        :return: None
        """
        self.inventory.remove(item)
        self.decrease_load(item)

    def decrease_load(self, item) -> None:
        """
        Decreases the current load of the container.

        :param dict item: The item to decrease load with.
        :return: None
        """
        self.load -= 1
