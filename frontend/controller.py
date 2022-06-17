"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

Controller.py
"""

import sys, os, time

class ApplicationController:
    def __init__(self):
        pass
    
    def end_application(self, onlychrome):
        if onlychrome == True:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")
        else:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")
            os.system("takskill /F /IM SmartLauncher* /T >nul 2>&1")
            sys.exit()
            
            ### --ONLY in TESTS-- os.system("taskkill /F /IM py* /T >nul 2>&1") ###
        
    def restart(self):
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        os.execl(sys.executable, sys.executable, *sys.argv)    

    
