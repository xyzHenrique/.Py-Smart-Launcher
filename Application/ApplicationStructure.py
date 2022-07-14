"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: Structure.py
version: 1.0.0
"""

### NATIVE
import os, time, json

### THIRD
import colorama

from ApplicationLogger import Logger

class Structure:
    def __init__(self):
        ### CALL and INITIALIZE THIRD PACKAGE
        colorama.init()

        ### CALL and INITIALIZE LOCAL PACKAGE
        self.structure = json.load(open("Structure"))

        self.logger = Logger()
        self.logger.InitializeLogger()

    def CheckFolderStructure(self):
        self.logger.WriteFile("Checking folder structure...", "INFO")

        err = list()

        for key in self.structure.keys():
            time.sleep(0.3)
            if not os.path.exists(self.structure[key]["dir"]):
                self.logger.WriteFile(f"{self.structure[key]['dir']}') doesn't exist! Closing application...", "CRITICAL")
            else:
                self.logger.WriteFile(f"('{self.structure[key]['dir']}') OK!", "DEBUG")

        return err

    def CheckFileStructure(self):
        self.logger.WriteFile("Checking file structure...", "INFO")

        err = list()

        for key in self.structure.keys():
            time.sleep(0.3)
            for file in self.structure[key]["files"]:
                if not os.path.exists(f"{self.structure[key]['dir']}/{file}"):
                    err.append(f"{self.structure[key]['dir']}/{file}")

                    self.logger.WriteFile(f"File ('{self.structure[key]['dir']}/{file}') doesn't exist!", "CRITICAL")
                else:   
                    self.logger.WriteFile(f"File ('{self.structure[key]['dir']}/{file}') OK!", "DEBUG")
        
        return err
        