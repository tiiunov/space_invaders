import random
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPainter, QPixmap
from entities.player import Player
from entities.alien import Alien
from entities.bullet import Bullet
from entities.wall import Wall
from entities.bonus import Bonus
from game_state import GameState


class GamePlay(QFrame):
    def __init__(self, field_wight, field_height):
        super().__init__()
        self.timer = QBasicTimer()
        self.score = 0
        self.time_counter = 0
        self.field_wight, self.field_height = field_wight, field_height
        self.is_started = self.is_finished = self.is_paused = False
        self.is_win = False
        self.timer_speed = 50
        self.shoot = self.ashoot = False
        self.player = Player(field_wight // 2, field_height - 35)
        self.pbullet = Bullet(-10, -10, 10)
        self.spec_pbullet = []
        self.spec_bullet_count = 0
        self.spec_pbullet_activated = self.spec_pbullet_is_fly = False
        self.spec_alien = Alien(-40, 35, -1)
        self.spec_alien_counter, self.spec_alien_is_here = 0, False
        self.bonus_counter, self.bonus_is_here = 0, False
        self.kills_to_bonus = 8
        self.bonus = Bonus(-50, -50)
        self.bullet_rain_started = False
        self.abullet = Bullet(-10, -10, 5)
        self.current_shooter = Alien(-1, -1, -1)
        self.alien_step_direction = 1
        self.bullet_rain = []
        self.aliens, self.walls, state_walls = [], [], []
        self.init_aliens()
        self.init_walls(self.walls)
        self.init_walls(state_walls)
        self.gameState = GameState(3, 5, self.player, state_walls)

    def init_aliens(self):
        y = 70
        for i in range(5):
            x = 25
            if i > 0:
                y += 30
            for j in range(10):
                self.aliens.append(Alien(x, y, j))
                x += 40

    def init_walls(self, walls):
        y = self.player.y - 30
        x = 30
        for i in range(5):
            walls.append(Wall(x, y))
            x += 100

    def start(self):
        self.is_started = True
        self.timer.start(self.timer_speed, self)

    def pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(self.timer_speed, self)
        self.update()

    def finish(self):
        self.is_finished = True
        self.is_started = False
        self.timer.stop()

    def win(self):
        self.is_win = True
        self.is_started = False
        self.timer.stop()

    def save_result(self):
        self.gameState.score = self.score
        self.gameState.timer_speed = self.timer_speed
        for i in range(0, 4):
            self.gameState.walls[i].health = self.walls[i].health

    def connect_result(self):
        self.score = self.gameState.score
        self.timer_speed = self.gameState.timer_speed
        self.player = self.gameState.player
        for i in range(0, 4):
            self.walls[i].health = self.gameState.walls[i].health

    def next_lvl(self):
        s = self.score
        h = self.player.health
        walls = self.walls
        t = self.timer_speed
        self.restart()
        self.walls = walls
        self.score = s
        self.player.health = h
        self.timer_speed = t - 5

    def restart(self):
        self.score = 0
        self.time_counter = 0
        self.is_started = self.is_finished = self.is_paused = False
        self.timer_speed = 50
        self.shoot = False
        self.player = Player(self.field_wight // 2, self.field_height - 35)
        self.pbullet = Bullet(-10, -10, 10)
        self.spec_alien = Alien(550, 35, -1)
        self.spec_alien_counter, self.spec_alien_is_here = 0, False
        self.bonus_counter, self.bonus_is_here = 0, False
        self.bonus = Bonus(-50, -50)
        self.alien_step_direction = 1
        self.aliens = []
        self.init_aliens()
        self.walls = []
        self.init_walls(self.walls)

    def timerEvent(self, event):
        if self.spec_alien_counter == 300:
            self.spec_alien.alive = True
            self.spec_alien_counter -= 300
            self.spec_alien_is_here = True
        if self.spec_alien_is_here and self.spec_alien_counter % 2 == 0:
            self.spec_alien_move()
        if self.shoot:
            if self.spec_pbullet_activated and not self.pbullet.isFly:
                self.shoot_spec_bullet()
            else:
                self.player_shooting()
        if self.ashoot:
            self.alien_shooting()
        if self.bonus_is_here:
            self.bonus_falling()
        if self.time_counter % 8 == 0:
            self.time_counter -= 8
            self.alien_standart_move()
            self.ashoot = True
        if self.bullet_rain_started:
            self.rain()
        self.time_counter += 1
        self.spec_alien_counter += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_pictures(painter)
        self.draw_up_table(painter)
        self.draw_gameplay(painter)

    def draw_up_table(self, painter):
        if self.is_paused:
            painter.drawPixmap(210, 3, QPixmap("pic/pause_pic.png"))
        painter.drawPixmap(3, 3, QPixmap("pic/score_pic.png"))
        x = 120
        for i in self.find_score_order():
            painter.drawPixmap(x, 3, QPixmap("pic/%d.png" % i))
            x += 18

    def draw_pictures(self, painter):
        if not self.is_started and not self.is_finished and not self.is_win:
            painter.drawPixmap(210, 3, QPixmap("pic/load_pic.png"))
            painter.drawPixmap(self.field_wight // 2 - 150,
                               self.field_height // 2,
                               QPixmap("pic/start_pic.png"))
        if self.is_finished:
            painter.drawPixmap(self.field_wight / 2 - 180,
                               self.field_height / 2 - 60,
                               QPixmap("pic/you_lose_pic.png"))
            painter.drawPixmap(210, 3, QPixmap("pic/load_pic.png"))
        if self.is_started:
            painter.drawPixmap(400, 3, QPixmap("pic/lives_pic.png"))
            painter.drawPixmap(440, 3,
                               QPixmap("pic/%d.png" % self.player.health))
        if self.is_win:
            painter.drawPixmap(self.field_wight / 2 - 180,
                               self.field_height / 2 - 60,
                               QPixmap("pic/win_pic.png"))
            painter.drawPixmap(self.field_wight / 2 - 180,
                               50,
                               QPixmap("pic/save_pic.png"))

    def draw_gameplay(self, painter):
        if self.player.health > 3:
            painter.drawPixmap(self.player.x, self.player.y,
                               QPixmap("pic/GunS.png"))
        else:
            painter.drawPixmap(self.player.x, self.player.y,
                               QPixmap("pic/Gun%d.png" % self.player.health))
        if self.pbullet.isFly:
            painter.drawPixmap(self.pbullet.x, self.pbullet.y,
                               QPixmap("pic/bullet.png"))
        painter.drawPixmap(self.abullet.x, self.abullet.y,
                           QPixmap("pic/bullet.png"))
        if self.spec_alien.alive:
            painter.drawPixmap(self.spec_alien.x,
                               self.spec_alien.y,
                               QPixmap("pic/spec alien.png"))
        painter.drawPixmap(self.bonus.x, self.bonus.y,
                           QPixmap("pic/bonus%d.png" % self.bonus.booster))
        for i in self.bullet_rain:
            painter.drawPixmap(i.x, i.y, QPixmap("pic/bullet.png"))
        for i in self.spec_pbullet:
            painter.drawPixmap(i.x, i.y, QPixmap("pic/bullet.png"))
        for i in self.aliens:
            if i.alive and not self.is_finished:
                painter.drawPixmap(i.x, i.y, QPixmap("pic/alien.png"))
        for w in self.walls:
            if w.health > 0:
                w_pic = "pic/wall%d.png" % w.health
                painter.drawPixmap(w.x, w.y, QPixmap(w_pic))

    def find_score_order(self):
        a = self.score
        b = []
        while a > 0:
            b.append(a % 10)
            a = a // 10
        b = b[::-1]
        return b

    def alien_standart_move(self):
        if self.alien_step_direction == 1:
            self.move_right()
        else:
            self.move_left()

    def move_right(self):
        max_ind = -1
        step_to_do = 0
        for i in self.aliens:
            if i.index > max_ind and i.alive:
                max_ind = i.index
        for i in self.aliens:
            if i.index == max_ind:
                if i.x + 36 < self.field_wight:
                    step_to_do = 1
                break
        if step_to_do == 1:
            for i in self.aliens:
                i.move(1)
        else:
            self.alien_step_direction *= -1
            for i in self.aliens:
                i.move(2)
                if i.y >= self.player.y - 5:
                    self.finish()

    def move_left(self):
        min_ind = 999
        step_to_do = 0
        for i in self.aliens:
            if i.index < min_ind and i.alive:
                min_ind = i.index
        for i in self.aliens:
            if i.index == min_ind:
                if i.x - 4 > 0:
                    step_to_do = 1
                break
        if step_to_do == 1:
            for i in self.aliens:
                i.move(-1)
        else:
            self.alien_step_direction *= -1
            for i in self.aliens:
                i.move(2)

    def spec_alien_move(self):
        if 0 <= self.spec_alien.x < self.field_wight - 30:
            self.spec_alien.move(1)
        elif self.spec_alien.x >= self.field_wight - 30:
            self.spec_alien_is_here = False
            self.spec_alien.x = -40
        else:
            self.spec_alien.x = 0

    def player_shooting(self):
        if not self.pbullet.isFly:
            self.pbullet.x = self.player.x + 13
            self.pbullet.y = self.player.y - 20
            self.pbullet.isFly = True
        elif self.pbullet.y > 30:
            if self.spec_alien.y <= self.pbullet.y <= \
                    self.spec_alien.y + 29 \
                    and self.spec_alien.x - 5 <= self.pbullet.x <= \
                    self.spec_alien.x + 30:
                self.spec_alien.alive = False
                self.score += 100
                self.stop_shooting()
            self.check_aliens_hit()
            for w in self.walls:
                if w.y <= self.pbullet.y <= w.down_bord \
                        and w.x - 7 <= self.pbullet.x <= w.right_bord:
                    w.health -= 1
                    if w.health >= 0:
                        self.stop_shooting()
                    if w.health < 0:
                        w.health = -1
            self.pbullet.fly(1)
        else:
            self.stop_shooting()

    def check_aliens_hit(self):
        alive_count = 0
        for i in self.aliens:
            if i.alive:
                alive_count += 1
            if i.y <= self.pbullet.y <= i.y + 15 \
                    and i.x - 3 <= self.pbullet.x <= i.x + 36:
                if i.alive:
                    i.alive = False
                    if i.y < self.field_height - 50:
                        self.bonus_counter += 1
                        if self.bonus_counter == self.kills_to_bonus:
                            self.bonus_counter -= 8
                            self.bonus.x = i.x + 10
                            self.bonus.y = i.y + 15
                            self.bonus_is_here = True
                    alive_count -= 1
                    self.score += 10
                    self.stop_shooting()
        if alive_count == 0:
            self.win()

    def stop_shooting(self):
        self.pbullet.isFly = False
        self.shoot = False
        self.pbullet.clear()

    def try_move(self, direction):
        if direction == 1 and self.player.x < self.field_wight - 36:
            self.player.move(1)
        if direction == -1 and self.player.x > 0:
            self.player.move(-1)
        self.update()

    def alien_shooting(self):
        if self.current_shooter.x == -1:
            self.choose_shooter()
        if not self.abullet.isFly:
            self.abullet.x = self.current_shooter.x + 18
            self.abullet.y = self.current_shooter.y + 24
            self.abullet.isFly = True
        elif self.abullet.y < self.field_height - 3:
            self.check_player_hit()
            for w in self.walls:
                if w.y - 3 <= self.abullet.y <= w.down_bord - 3 \
                        and w.x - 7 <= self.abullet.x <= w.right_bord:
                    w.health -= 1
                    if w.health >= 0:
                        self.stop_alien_shooting()
                    if w.health < 0:
                        w.health = -1
            self.abullet.fly(-1)
        else:
            self.stop_alien_shooting()

    def choose_shooter(self):
        potential_shooters = []
        indexes = []
        for i in self.aliens[::-1]:
            if i.index not in indexes and i.alive:
                potential_shooters.append(i)
                indexes.append(i.index)
        self.current_shooter = \
            potential_shooters[random.randint(0,
                                              len(potential_shooters) - 1)]

    def check_player_hit(self):
        if self.player.y - 5 <= self.abullet.y <= self.player.y + 30 \
                and self.player.x - 8 <= self.abullet.x \
                <= self.player.x + 36:
            self.player.health -= 1
            self.stop_alien_shooting()
            if self.player.health < 0:
                self.finish()

    def stop_alien_shooting(self):
        self.abullet.isFly = False
        self.ashoot = False
        self.abullet.clear()
        self.current_shooter = Alien(-1, -1, -1)

    def bonus_falling(self):
        if self.bonus.y < self.field_height - 20:
            if self.player.y - 25 <= self.bonus.y <= self.player.y \
                    and self.player.x - 18 <= self.bonus.x \
                    <= self.player.x + 36:
                if self.bonus.booster == 1 and self.player.health < 5:
                    self.player.health += 1
                    self.delete_bonus()
                elif self.bonus.booster == 2:
                    self.init_spec_pbullet()
                    self.delete_bonus()
                elif self.bonus.booster == 3:
                    self.start_bullet_rain()
                    self.delete_bonus()
            self.bonus.move()
        else:
            self.delete_bonus()

    def delete_bonus(self):
        self.bonus.clear()
        self.bonus.upgrade()

    def start_bullet_rain(self):
        self.bullet_rain_started = True
        y = self.player.y - 45
        x = 5
        for i in range(16):
            self.bullet_rain.append(Bullet(x, y, 10))
            x += 30

    def rain(self):
        for b in self.bullet_rain:
            if b.y > 30:
                if self.spec_alien.y <= b.y <= \
                        self.spec_alien.y + 29 \
                        and self.spec_alien.x - 5 <= b.x <= \
                        self.spec_alien.x + 30:
                    self.spec_alien.alive = False
                    self.score += 100
                    b.clear()
                alive_count = 0
                for i in self.aliens:
                    if i.alive:
                        alive_count += 1
                    if i.y <= b.y <= i.y + 15 \
                            and i.x - 3 <= b.x <= i.x + 36:
                        if i.alive:
                            i.alive = False
                            alive_count -= 1
                            self.score += 10
                            b.clear()
                if alive_count == 0:
                    self.win()
                b.fly(1)
            else:
                b.clear()

    def init_spec_pbullet(self):
        for i in range(3):
            self.spec_pbullet.append(Bullet(-10, -10, 10))
        self.spec_bullet_count = 7
        self.spec_pbullet_activated = True

    def shoot_spec_bullet(self):
        ind = -1
        if not self.spec_pbullet_is_fly:
            self.run_spec_pbullet()
        for b in self.spec_pbullet:
            ind += 1
            if b.y > 30:
                self.check_salien_hit(b)
                self.check_alien_hit(b)
                for w in self.walls:
                    if w.y <= b.y <= w.down_bord \
                            and w.x - 7 <= b.x <= w.right_bord:
                        w.health -= 1
                        if w.health >= 0:
                            self.end_spec_shoot(b)
                        if w.health < 0:
                            w.health = -1
                if ind == 0:
                    b.fly(1)
                if ind == 1:
                    b.fly(2)
                if ind == 2:
                    b.fly(-2)
            else:
                self.end_spec_shoot(b)

    def run_spec_pbullet(self):
        self.spec_bullet_count -= 1
        if self.spec_bullet_count == 0:
            self.spec_pbullet.clear()
            self.spec_pbullet_activated = False
            return
        for b in self.spec_pbullet:
            b.x = self.player.x + 13
            b.y = self.player.y + 5
            b.isFly = True
        self.spec_pbullet_is_fly = True

    def check_salien_hit(self, b):
        if self.spec_alien.y <= b.y <= \
                self.spec_alien.y + 29 \
                and self.spec_alien.x - 5 <= b.x <= \
                self.spec_alien.x + 30:
            self.spec_alien.alive = False
            self.score += 100
            b.clear()

    def check_alien_hit(self, b):
        alive_count = 0
        for i in self.aliens:
            if i.alive:
                alive_count += 1
            if i.y <= b.y <= i.y + 15 \
                    and i.x - 3 <= b.x <= i.x + 36:
                if i.alive:
                    i.alive = False
                    alive_count -= 1
                    self.score += 10
                    self.end_spec_shoot(b)
        if alive_count == 0:
            self.win()

    def check_specbull_end(self):
        for b in self.spec_pbullet:
            if b.isFly:
                return False
        return True

    def end_spec_shoot(self, b):
        b.clear()
        b.isFly = False
        if self.check_specbull_end():
            self.spec_pbullet_is_fly = False
            self.shoot = False
