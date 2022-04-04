"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

controller.py
"""

import sys, os, time

class ApplicationController:
    def __init__(self):
        pass
    
    def end(self, onlychrome):
        if onlychrome == True:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")
        else:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")
            ### --ONLY TESTS-- os.system("taskkill /F /IM py* /T >nul 2>&1") ###
            os.system("takskill /F /IM S2SLauncher* /T >nul 2>&1")

            sys.exit()
        
    def restart(self):
        time.sleep(0.50)
        os.system("cls" if os.name == "nt" else "clear")
        os.execl(sys.executable, sys.executable, *sys.argv)    

    
