from models.containers.Container import Container


class RocketSilo(Container):
    """
    A container for holding items to be launched. Has a capacity of 1000 kg
    which determines the maximum weight of items that can be added to it.

    Inherits from Container.

    Attributes:
        container (str): The name of the container.
        capacity (int): The maximum weight that can be added to the silo.
        inventory (list): A list of items in the rocket silo.
    """

    def __init__(self):
        super().__init__(container="rocket_silo", capacity=1000)

    def can_add_item(self, item):
        """
        Checks if the container has enough space to add an item.

        :param dict item: The item to check.
        :return: True if the container has enough space to add an item,
        False otherwise.
        :rtype: bool
        """
        if self.load + item["weight"] <= self.capacity:
            return True
        return False

    def increase_load(self, item):
        """
        Increases the current load of the rocket silo using the item's weight.

        :param dict item: The item to increase load weight with.
        :return: None
        """
        self.load += item["weight"]

    def decrease_load(self, item):
        """
        Decreases the current load of the rocket silo using the item's weight.

        :param dict item: The item to decrease load weight with.
        :return: None
        """
        self.load -= item["weight"]