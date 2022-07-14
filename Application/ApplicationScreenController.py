"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: ApplicationScreenController.py
version: 1.0.0
"""

### NATIVE
import os, json, time, threading

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

            self.logger.WriteFile(f"Screen: ({self.screens['connected']}) registred!", "INFO")

        with open(f"{self.structure['Application.Data']['dir']}/{self.structure['Application.Data']['files'][0]}", "w+") as outfile:
            outfile.write(str(self.screens["connected"]))
        
        threading.Thread(target=self.ScreenThreading, args=()).start()

    def ScreenThreading(self):
        while True:
            
            time.sleep(15)

            for monitor in screeninfo.get_monitors():
                if monitor != self.screens["connected"]:
                    self.logger.WriteFile(f"monitor: {monitor} connected!", "INFO")
                else:
                    self.logger.WriteFile(f"monitor: {monitor} disconnected!", "WARNING")