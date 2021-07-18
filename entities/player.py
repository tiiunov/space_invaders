from entities.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 3
