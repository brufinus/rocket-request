class Container:
    """
    Abstract base class for containers.

    Attributes:
        container (str): The name of the container.
        capacity (int): The maximum amount the container can have.
        inventory (list): A list of items in the container.
    """

    def __init__(self, container, capacity):
        self.container = container
        self.capacity = capacity
        self.inventory = []

    def add_item(self, item):
        """
        Adds an item to the container.

        :param Item item: The item to add.
        :return: None
        """
        self.inventory.append(item)

    def remove_item(self, item):
        """
        Removes an item from the container.

        :param Item item: The item to remove.
        :return: None
        """
        self.inventory.remove(item)
