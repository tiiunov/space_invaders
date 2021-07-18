from entities.base_entity import BaseEntity


class Alien(BaseEntity):
    def __init__(self, x, y, ind):
        super().__init__(x, y)
        self.alive = True
        self.index = ind
