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

    def __init__(self) -> None:
        super().__init__(container="rocket_silo", capacity=1000)

    def can_add_item(self, item: dict[str, str | int]) -> bool:
        """
        Checks if the rocket silo has enough empty weight to add an item.
        Overrides Container.can_add_item.

        :param dict item: The item to check.
        :return: Whether the silo has enough empty weight to add an item.
        :rtype: bool
        """
        if self.load + int(item["weight"]) <= self.capacity:
            return True
        return False

    def increase_load(self, item: dict[str, str | int]) -> None:
        """
        Increases the current load of the rocket silo using the item's weight.
        Overrides Container.increase_load.

        :param dict item: The item to increase load weight with.
        :return: None
        """
        self.load += int(item["weight"])

    def decrease_load(self, item: dict[str, str | int]) -> None:
        """
        Decreases the current load of the rocket silo using the item's weight.
        Overrides Container.decrease_load.

        :param dict item: The item to decrease load weight with.
        :return: None
        """
        self.load -= int(item["weight"])