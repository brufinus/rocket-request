"""
Defines the Container abstract base class.

Classes:
    Container: An abstract base class that defines container structure.
"""

from abc import ABC, abstractmethod

from data.item import Item


class Container(ABC):
    """
    Abstract base class for containers.
    
    A container is a storage unit that can hold items.

    Public methods: add_item, can_add_item, increase_load, remove_item,
    decrease_load
    
    Instance variables: container, capacity, inventory, load
    """

    def __init__(self, container: str, capacity: int) -> None:
        """
        Initializes a container with a name and capacity.
        
        :param str container: The name of the container.
        :param int capacity: The maximum amount the container can have.
        :return: None
        """
        self.container = container
        self.capacity = capacity
        self.inventory: list[Item] = []
        self.load: float = 0

    def add_item(self, item: Item) -> bool:
        """
        Adds an item to the container.

        Appends the item to the inventory and increases load.

        :param Item item: The item to add.
        :return: Whether the item was added to the container.
        :rtype: bool
        """
        if self.can_add_item(item):
            self.inventory.append(item)
            self.increase_load(item)
            return True
        return False

    @abstractmethod
    def can_add_item(self, item) -> bool:
        """Return whether the container has space to add an item."""

    @abstractmethod
    def increase_load(self, item) -> None:
        """Increases the load of the container with the item weight."""

    def remove_item(self, item) -> None:
        """
        Removes an item from the inventory and decreases load.

        :param item: The item to remove.
        :return: None
        """
        self.inventory.remove(item)
        self.decrease_load(item)

    @abstractmethod
    def decrease_load(self, item: Item) -> None:
        """Subtracts the weight of the item from the container load."""
