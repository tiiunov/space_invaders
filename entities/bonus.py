import random
from entities.base_entity import BaseEntity


class Bonus(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.booster = self.chose_booster(random.randint(1, 10))

    @staticmethod
    def chose_booster(i):
        if i < 5:
            return 2
        if i < 8:
            return 3
        return 1

    def move(self, **kwargs):
        self.y += 3

    def clear(self):
        self.x = -50
        self.y = -50

    def upgrade(self):
        self.booster = self.chose_booster(random.randint(1, 10))
