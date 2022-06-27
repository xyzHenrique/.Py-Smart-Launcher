"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: ApplicationScreenController.py
version: 1.0.0
"""

### NATIVE
import os, json

### THIRD
import screeninfo

### LOCAL
from ApplicationLogger import Logger

class ScreenController:
    def __init__(self):
        ### CALL and INITIALIZE LOCAL PACKAGE
        self.structure = json.load(open("Structure"))
        
        self.logger = Logger()
        self.logger.InitializeLogger()

        ### ... ###
        self.screens = {
            "connected": list(),
            "disconnected": list(),
        }

    def ScreenRegister(self):
        for screen in screeninfo.get_monitors():
            self.screens["connected"].append(screen)

        self.logger.WriteFile(f"Connected screens: ({self.screens['connected']})", "INFO")

        with open(f"{self.structure.structure['Application.Data']['dir']/self.structure.structure['Application.Data']['files']['data.dat']}", "w+") as outfile:
            outfile.write(self.screens["connected"])

    def ScreenThreading(self):
        for monitor in screeninfo.get_monitors():
            if monitor in self.connected_screens:
                pass
            else:
                self.module_logger.write_file("WARNING", f"monitor: {monitor} disconnected!")
        
            print(monitor)

x = ScreenController().ScreenRegister()