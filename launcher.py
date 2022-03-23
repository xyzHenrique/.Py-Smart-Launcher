from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from application import Application, version
from updater import ApplicationUpdater
from controller import ApplicationController

import sys, os, time

class ApplicationLauncher:
    def __init__(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False) 

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("./system/images/logo.png"))
        self.tray.setVisible(True)

        self.controller = ApplicationController()

        self.check_updates(ApplicationUpdater())
        self.tray_run()
    
    def tray_run(self):
        menu = QMenu()  

        name = QAction(f"S2SLauncher {version}")
             
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

        def click_option3():
            print("- selecionado: 'verificar atualizações'\n\ruma nova verificação será feita\n\n\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            self.check_updates(ApplicationUpdater())
        
        def click_option4():
            print("- selecionado: 'reiniciar'\n\ra aplicação será reiniciada\n\n\n")
            time.sleep(1) 
            self.controller.restart()
            
            
        def click_option5():
            print("- selecionado: 'sair'\n\rsaindo da aplicação\n\n\n")
            time.sleep(1)
            self.app.quit
            self.controller.end(onlychrome=False)
            sys.exit()

        option3.triggered.connect(click_option3)
        
        option4.triggered.connect(click_option4)

        option5.triggered.connect(click_option5)

        self.tray.setContextMenu(menu)

        self.app.exec_()

    def check_updates(self, updater):
        updated, versions = updater.check_version()

        if not updated:
            print(f"- atualizado: (c-{versions[0]} / l-{versions[1]})\n")

            Application()
        else:
            print(f"- desatualizado: (c-{versions[0]} / l-{versions[1]})\n")

            if updater.download(versions[1]):
                Application()
                pass

ApplicationLauncher()