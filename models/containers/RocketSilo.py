from data.constants import ITEM_WEIGHT
from data.item import Item
from models.containers.Container import Container


class RocketSilo(Container):
    """
    A container for holding items to be launched.

    Has a capacity of 1000 kg which is the maximum
    weight of items that can be added to it.

    Subclasses Container.

    Attributes:
        CAPACITY (int): The maximum weight that
                        can be added to the silo.
    """

    CAPACITY: int = 1000
    "The maximum weight that can be added to the silo."

    def __init__(self) -> None:
        """
        Initializes a rocket silo container.

        Extends Container.__init__
        """
        super().__init__(container="rocket_silo",
                         capacity=self.CAPACITY)

    def can_add_item(self, item: Item) -> bool:
        """
        Check whether an item can be added to the rocket silo.

        Determines whether the silo has enough remaining
        capacity to add the item's weight.

        Overrides Container.can_add_item

        :param Item item: The item to check.
        :return: Whether the silo has space to add an item.
        :rtype: bool
        """
        if self.load + float(item[ITEM_WEIGHT]) <= self.capacity:
            return True
        return False

    def increase_load(self, item: Item) -> None:
        """
        Increases the load of the rocket silo by the item's weight.

        Overrides Container.increase_load

        :param Item item:
        The item to increase load weight by.
        :return: None
        """
        self.load += float(item[ITEM_WEIGHT])

    def decrease_load(self, item: Item) -> None:
        """
        Decreases the load of the rocket silo by the item's weight.

        Overrides Container.decrease_load

        :param Item item:
        The item to decrease load weight by.
        :return: None
        """
        self.load -= float(item[ITEM_WEIGHT])
