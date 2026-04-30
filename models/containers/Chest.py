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