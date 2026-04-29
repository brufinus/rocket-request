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
