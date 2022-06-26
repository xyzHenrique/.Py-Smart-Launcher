"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: Controllers.py
version: 3.0.0
"""
### NATIVE
import os, sys, time, threading, time

### THIRD
import screeninfo

### LOCAL
from ApplicationInformation import *
from Modules.Logger import ApplicationLogger

class ApplicationController:
    def __init__(self):
        self.command_windows_application_kill = f"takskill /F /IM {APP_INFORMATIONS['APP_NAME']}* /T >nul 2>&1"
        self.command_windows_engine_kill = "taskkill /F /IM chrome* /T >nul 2>&1"
        
    def application_kill(self):
        if os.name == "nt":
            os.system(self.command_windows_application_kill)
    
    def application_restart(self):
        if os.name == "nt":
            os.execl(sys.executable, sys.executable, *sys.argv)    
    
    def engine_kill(self):
        if os.name == "nt":
            os.system(self.command_windows_engine_kill)
        
class ScreenController:
    def __init__(self):
        self.module_logger = ApplicationLogger()

        self.connected_screens = list()
        self.disconnected_screens = list()

        self.register_screens()

    def register_screens(self):
        for screen in screeninfo.get_monitors():
            self.connected_screens.append(screen)

        with open(f"./data/{APP_DATA['session_data']}", "w+") as outfile:
            outfile.write(str(self.connected_screens))

            thread = threading.Thread(target=self.manager_monitors, args=(), daemon=True)
            thread.start()

    def manager_monitors(self):
        while True:
            time.sleep(30)
        
            for monitor in screeninfo.get_monitors():
                if monitor in self.connected_screens:
                    pass
                else:
                    self.module_logger.write_file("WARNING", f"monitor: {monitor} disconnected!")
            
                print(monitor)

x = MonitorsController()