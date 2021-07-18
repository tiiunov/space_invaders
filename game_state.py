

class GameState:
    def __init__(self, score, timer_speed, player, walls):
        self.score = score
        self.timer_speed = timer_speed
        self.player = player
        self.walls = walls

    def save(self):
        save = f"{self.score};{self.timer_speed};" \
               f"{self.player.x};{self.player.y};" \
               f"{self.player.health};{self.walls[0].health};" \
               f"{self.walls[1].health};{self.walls[2].health};" \
               f"{self.walls[3].health};{self.walls[4].health}"
        with open('saves.txt', 'w') as f:
            f.write(save)

    @staticmethod
    def try_load():
        with open('saves.txt', 'r') as f:
            save = f.readline().split(';')
        return len(save) == 10

    def load(self):
        with open('saves.txt', 'r') as f:
            save = f.readline().split(';')
        self.score = int(save[0])
        self.timer_speed = int(save[1])
        self.player.x = int(save[2])
        self.player.y = int(save[3])
        self.player.health = int(save[4])
        for i in range(0, 4):
            self.walls[i].health = int(save[5 + i])
