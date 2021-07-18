import unittest
import entities.player as p
import entities.bullet as b
import entities.alien as a
import entities.wall as w
import entities.bonus as bon


class MyTest(unittest.TestCase):
    def setUp(self):
        self.player = p.Player(250, 250)
        self.bullet = b.Bullet(250, 250, 10)
        self.alien = a.Alien(50, 100, -1)
        self.wall = w.Wall(400, 400)
        self.bonus = bon.Bonus(300, 300)

    def test_player_opportunities(self):
        expected_coordinate = 200
        self.assertEqual(self.player.health, 3)
        for i in range(3):
            self.player.move(1)
        for i in range(13):
            self.player.move(-1)
        self.assertEqual(self.player.x, expected_coordinate)
        self.player.health -= 2
        self.assertEqual(self.player.health, 1)

    def test_bullet(self):
        expected_sleep_x = expected_sleep_y = -10
        expected_y = 300
        for i in range(228):
            self.bullet.fly(-1)
        for i in range(223):
            self.bullet.fly(1)
        self.assertEqual(self.bullet.y, expected_y)
        self.bullet.clear()
        self.assertEqual(self.bullet.x, expected_sleep_x)
        self.assertEqual(self.bullet.y, expected_sleep_y)

    def test_alien_opportunities(self):
        expected_coordinate_x = expected_coordinate_y = 300
        self.assertEqual(self.alien.alive, True)
        for i in range(3):
            self.alien.move(-1)
        for i in range(53):
            self.alien.move(1)
        for i in range(20):
            self.alien.move(2)
        self.assertEqual(self.alien.x, expected_coordinate_x)
        self.assertEqual(self.alien.y, expected_coordinate_y)

    def test_bonus(self):
        expected_bonus_y = 330
        expected_sleep_x = expected_sleep_y = -50
        self.assertTrue(self.in_border(self.bonus.booster))
        for i in range(10):
            self.bonus.move()
        self.assertEqual(expected_bonus_y, self.bonus.y)
        self.bonus.clear()
        self.assertEqual(self.bonus.x, expected_sleep_x)
        self.assertEqual(self.bonus.y, expected_sleep_y)

    @staticmethod
    def in_border(i):
        return i == 1 or i == 2 or i == 3


if __name__ == '__main__':
    unittest.main()
