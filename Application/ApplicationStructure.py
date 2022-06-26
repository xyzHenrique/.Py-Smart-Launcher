"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: Structure.py
version: 1.0.0
"""

### NATIVE
import os

### LOCAL
#from ApplicationLogger import ApplicationLogger

class Structure:
    def __init__(self):
        self.structure = {
            "Application.Data": {
                "dir": "Application/Data",
                "files": [
                    "data.dat"
                    ]
            },

            "Application.Engine": {
                "dir": "Application/Engine",
                "files": []
            },

            "Application.Logs": {
                "dir": "Application/Logs",
                "files": []
            },

            "Application.Plugins": {
                "dir": "Application/Plugins",
                "files": []
            },

            "Application.Presets": {
                "dir": "Application/Presets",
                "files": []
            },

            "Application.Settings": {
                "dir": "Application/Settings",
                "files": [
                    "ApplicationSettings.json",
                    "AutomationSettings.json",
                ]
            },
        }
    
    def CheckStructure(self):
        ### CHECK for PRIMARY FOLDERS
        for folder in self.structure["primary-folders"]:
            if os.path.exists(f"{folder}"):
                self.module_logger.write_file("INFO", f"folder ('{folder}') OK!")
            else:
                self.module_logger.write_file("WARNING", f"folder ('{folder}') does not exist!")
                
                if not folder == self.structure["important-folders"]:
                    self.module_logger.write_file("CRITICAL", f"a critical folder ({folder}) is not available!")
                else:
                    create = os.getcwd()+"/"+f"{folder}"

                    if not os.path.exists(create):
                        os.makedirs(create)

                        self.module_logger.write_file("INFO", f"folder ('{create}') successfully created!")
                    else:
                        self.module_logger.write_file("WARNING", f"could not create folder ('{create}') ")