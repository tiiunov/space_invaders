
class BaseEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == 2:
            self.y += 10
        else:
            self.x += 5 * direction

