from models.containers.Container import Container


class RocketSilo(Container):
    def __init__(self):
        super().__init__(container="rocket_silo", capacity=1000)
