from models.containers.Container import Container


class Chest(Container):
    """
    A standard storage container for holding items. Has a capacity of 48
    slots which can hold full stacks of items.

    Inherits from Container.

    Attributes:
        container (str): The name of the container.
        capacity (int): The maximum number of slots available.
        inventory (list): A list of items in the chest.
    """

    def __init__(self) -> None:
        super().__init__(container="chest", capacity=48)

    def can_add_item(self, item) -> bool:
        """
        Checks if the chest has enough slots to add an item.
        Overrides Container.can_add_item.
        TODO: Implement stack size checking for items that can be stacked.

        :param dict item: The item to insert.
        :return: Whether the chest has enough slots to add an item.
        :rtype: bool
        """
        if self.load + 1 <= self.capacity:
            return True
        return False
    
    def increase_load(self, item) -> None:
        """
        Increases the current load of the chest by 1 slot.
        Overrides Container.increase_load.
        TODO: Implement stack size checking for items that can be stacked.

        :param dict item: The item to increase load with.
        :return: None
        """
        self.load += 1
    
    def decrease_load(self, item) -> None:
        """
        Decreases the current load of the chest by 1 slot.
        Overrides Container.decrease_load.
        TODO: Implement stack size checking for items that can be stacked.

        :param dict item: The item to decrease load with.
        :return: None
        """
        self.load -= 1