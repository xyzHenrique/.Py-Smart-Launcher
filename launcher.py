from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from application import Application
from update import ApplicationUpdate

import sys, time

class ApplicationTray:
    def __init__(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False) 

        self.update = ApplicationUpdate()

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("./system/images/logo.png"))
        self.tray.setVisible(True)
    
        self.tray_run()
    
    def startup_update(self):
        """ get update """
        self.updated, self.versions = self.update.check_version()

        print("conferindo atualização...")
        time.sleep(1.5)

        if not self.updated:
            print(f"- atualizado: (c-{self.versions[0]} / l-{self.versions[1]})\n")

            #Application()  

        else:
            print(f"desatualizado: (c-{self.versions[0]} / l-{self.versions[1]})\n")

            self.update.download(self.versions[1])
    
    def startup_path(self):
        """ get path """
        with open("./system/session", "w") as file:
            file.write(sys.argv[0])

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

        """ FUNCTIONS """
        self.startup_update()
        self.startup_path()

        self.app.exec_()

ApplicationTray()