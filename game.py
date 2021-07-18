import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from gameplay import GamePlay


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gameplay = GamePlay(500, 500)
        self.setCentralWidget(self.gameplay)
        self.gameplay.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setFixedSize(500, 500)
        self.setWindowTitle('Space Invaders')

    def keyPressEvent(self, e):
        if self.gameplay.is_started:
            if e.key() == Qt.Key_A:
                self.gameplay.try_move(-1)
            if e.key() == Qt.Key_D:
                self.gameplay.try_move(1)
            if e.key() == Qt.Key_Space:
                self.gameplay.shoot = True
            if e.key() == Qt.Key_Escape:
                self.gameplay.pause()
        if not self.gameplay.is_win:
            if e.key() == Qt.Key_S:
                self.gameplay.start()
        if not self.gameplay.is_started:
            if e.key() == Qt.Key_L:
                if self.gameplay.gameState.try_load():
                    self.gameplay.gameState.load()
                    self.gameplay.connect_result()
        if self.gameplay.is_finished:
            if e.key() == Qt.Key_L:
                if self.gameplay.gameState.try_load():
                    self.gameplay.restart()
                    self.gameplay.gameState.load()
                    self.gameplay.connect_result()
                    self.gameplay.start()
            if e.key() == Qt.Key_R:
                self.gameplay.restart()
                self.gameplay.start()
        if self.gameplay.is_win:
            if e.key() == Qt.Key_F:
                self.gameplay.save_result()
                self.gameplay.gameState.save()
            if e.key() == Qt.Key_N:
                self.gameplay.next_lvl()
                self.gameplay.start()
                self.gameplay.is_win = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Game()
    myapp.show()
    sys.exit(app.exec_())
