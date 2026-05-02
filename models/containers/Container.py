from abc import ABC, abstractmethod


class Container(ABC):
    """
    Abstract base class for containers.

    Attributes:
        container (str): The name of the container.
        capacity (int): The maximum amount the container can have.
        inventory (list): A list of items in the container.
        load (float): The current load of the container.
    """

    def __init__(self, container: str, capacity: int) -> None:
        self.container = container
        self.capacity = capacity
        self.inventory: list[dict[str, str | float]] = []
        self.load: float = 0

    def add_item(self, item: dict[str, str | float]) -> bool:
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

    @abstractmethod
    def can_add_item(self, item: dict[str, str | float]) -> bool:
        """
        Checks if the container has enough space to add an item.

        :param dict item: The item to insert.
        :return: Whether the container has enough space to add an item.
        :rtype: bool
        """
        pass

    @abstractmethod
    def increase_load(self, item: dict[str, str | float]) -> None:
        """
        Increases the current load of the container using the given item.

        :param dict item: The item to increase load with.
        :return: None
        """
        pass

    def remove_item(self, item: dict[str, str | float]) -> None:
        """
        Removes an item from the container.

        :param dict item: The item to remove.
        :return: None
        """
        self.inventory.remove(item)
        self.decrease_load(item)

    @abstractmethod
    def decrease_load(self, item: dict[str, str | float]) -> None:
        """
        Decreases the current load of the container.

        :param dict item: The item to decrease load with.
        :return: None
        """
        pass
