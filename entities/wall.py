from entities.base_entity import BaseEntity


class Wall(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 10
        self.right_bord = x + 40
        self.down_bord = y + 8

    def move(self, **kwargs):
        pass
