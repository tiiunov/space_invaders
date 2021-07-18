from entities.base_entity import BaseEntity


class Bullet(BaseEntity):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed
        self.isFly = False

    def fly(self, direction):
        if abs(direction) == 1:
            self.y += self.speed * direction * -1
        elif direction == 2:
            self.y += self.speed * -1
            self.x += 3
        else:
            self.y += self.speed * -1
            self.x -= 3

    def clear(self):
        self.x = -10
        self.y = -10
