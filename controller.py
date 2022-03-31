import sys, os, time

class ApplicationController:
    def __init__(self):
        pass
    
    def end(self, onlychrome):
        if onlychrome == True:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")
            ### sys.exit()
        else:
            os.system("taskkill /F /IM S2SLauncher* /T >nul 2>&1")
            sys.exit()

    def restart(self):
        time.sleep(1.5)
        os.system("cls" if os.name == "nt" else "clear")
        os.execl(sys.executable, sys.executable, *sys.argv)    

    
