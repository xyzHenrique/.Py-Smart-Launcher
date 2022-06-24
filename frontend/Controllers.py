"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

Controllers.py
"""
import sys, os, time, threading, screeninfo

from Informations import *

from modules.Logger import ApplicationLogger

class ChromeController:
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

class MonitorsController:
    def __init__(self):
        self.module_logger = ApplicationLogger()

        self.connected_monitors = list()
        self.disconnected_monitors = list()

        self.register_monitors()

    def register_monitors(self):
        for monitor in screeninfo.get_monitors():
            self.connected_monitors.append(monitor)

        with open(f"./data/{APP_DATA['session_data']}", "w+") as outfile:
            outfile.write(str(self.connected_monitors))

            thread = threading.Thread(target=self.manager_monitors, args=(), daemon=True)
            thread.start()

    def manager_monitors(self):
        while True:
            time.sleep(30)
        
            for monitor in screeninfo.get_monitors():
                if monitor in self.connected_monitors:
                    pass
                else:
                    self.module_logger.write_file("WARNING", f"monitor: {monitor} disconnected!")
            
                print(monitor)

x = MonitorsController()