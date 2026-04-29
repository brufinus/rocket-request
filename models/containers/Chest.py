from models.containers.Container import Container


class Chest(Container):
    def __init__(self):
        super().__init__(container="chest", capacity=48)