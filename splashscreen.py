from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

class Splashscreen:
    def __init__(self):
        self.app = QApplication([])

        self.splash = QSplashScreen()
        self.splash.setPixmap(QPixmap("./system/images/app.png"))

        self.run()
    
    def run(self):
        QTimer.singleShot(3000, self.splash.close)

        self.splash.show()
        self.app.exec_()

x = Splashscreen()
