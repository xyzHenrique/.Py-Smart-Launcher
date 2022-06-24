import os
from struct import Struct

from modules.Logger import ApplicationLogger

class Structure:
    def __init__(self):
        self.module_logger = ApplicationLogger()
        
        self.structure = {
            "primary-folders": {
                "data",
                "logs",
                "system"
            },

            "subfolders": {
                "system/presets"
            },

            "files": {
                "data/data.dat",
                "system/settings.json"
            }
        }

    def check(self):
        ### CHCECK STRUCTURE V1.0.0 ###

        ### CHECK for PRIMARY FOLDERS
        for folder in self.structure["primary-folders"]:
            path = os.path.exists(f"{folder}")

            if path:
                self.module_logger.write_file("INFO", f"folder ('{folder}') OK!")
            else:
                self.module_logger.write_file("WARNING", f"folder ('{folder}') does not exist")

                create = os.getcwd()+"/"+f"{folder}"

                if not os.path.exists(create):
                    os.makedirs(create)

                    self.module_logger.write_file("INFO", f"folder ('{create}') successfully created")
                else:
                    self.module_logger.write_file("WARNING", f"could not create folder ('{create}') ")


x = Structure().check()