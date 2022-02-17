from application import Application

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from update import ApplicationUpdate

class ApplicationTray:
    def __init__(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

        self.update = ApplicationUpdate()

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("./system/images/logo.png"))
        self.tray.setVisible(True)
        
        self.tray_run()
    
    def tray_run(self):
        menu = QMenu()  

        name = QAction(f"S2SLauncher 3.6.2")
             
        option1 = QAction("minimizar")
        option2 = QAction("maximizar")

        option3 = QAction("verificar atualizações")
        
        option4 = QAction("reiniciar")
        option5 = QAction("sair")

        menu.addAction(name)
        menu.addSeparator()
    
        menu.addAction(option1)
        menu.addAction(option2)
        
        menu.addSeparator()
        menu.addAction(option3)
        menu.addSeparator()
        
        menu.addAction(option4)
        menu.addAction(option5)

        option5.triggered.connect(self.app.quit)

        self.tray.setContextMenu(menu)

        """ check update """
        self.updated, self.versions = self.update.check_version()

        if not self.updated:
            print(f"'chromedriver' está atualizado: (c-{self.versions[0]} / l-{self.versions[1]})")

            Application()  

        else:
            print(f"'chromedriver' está desatualizado: (c-{self.versions[0]} / l-{self.versions[1]})")

            self.update.download(self.versions[1])

        self.app.exec_()

ApplicationTray()