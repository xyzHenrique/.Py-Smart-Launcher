"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

modules > settings.py | v2 |
"""

import json

from ApplicationCheckStructure import 

def ApplicationSettings():
    def __init__(self):
        pass

    def 
    try:
        data_settings = json.load(open("./system/settings.json"))
        data_monitors = json.load(open(f"./system/presets/{data_settings['MONITORS']['.PRESET']}/preset.json"))
        
        with open("versions", "r") as file:
            data = json.load(file)

            data_software_version = data["SOFTWARE_VERSION"]
            data_driver_version = data["DRIVER_VERSION"]

        return data_settings, data_monitors, data_software_version, data_driver_version
    except Exception as err:
        print(err)



"""APPLICATION"""
self.settings_general_application = {
    "URL": self.settings_general["APPLICATION"][".URL"],
    "application-automatic-update": self.settings_general["APPLICATION"][".APPLICATION-AUTOMATIC-UPDATE"],
    "driver-automatic-update": self.settings_general["APPLICATION"][".DRIVER-AUTOMATIC-UPDATE"],
    "driver-manual": {
        "enabled": self.settings_general["APPLICATION"][".DRIVER-MANUAL"][".ENABLED"]
    }
    
    }

"""BLOCK"""
self.settings_general_block = {
    "enabled": self.settings_general["BLOCK"][".ENABLED"],
    "url": self.settings_general["BLOCK"][".URL"]
}

"""SYSTEM"""
self.settings_general_system = {
    "secure-exit": {
        "enabled": self.settings_general["SYSTEM"][".SECURE-EXIT"][".ENABLED"],
        "keys": self.settings_general["SYSTEM"][".SECURE-EXIT"][".KEYS"]
    },

    "secure-start": self.settings_general["SYSTEM"][".SECURE-START"]
}

"""AUTOMATION"""
self.settings_general_automation = {
    "automation": {
        "enabled": self.settings_general["AUTOMATION"][".ENABLED"],
    },

    "timer": {
        "enabled": self.settings_general["AUTOMATION"][".TIMER"][".ENABLED"],
        "time": self.settings_general["AUTOMATION"][".TIMER"][".TIME"]
    },

    "show": self.settings_general["AUTOMATION"][".SHOW"],
    "keys": self.settings_general["AUTOMATION"][".KEYS"]
}

"""DEV"""
self.settings_general_dev = {
    "enabled": self.settings_general["DEV"][".ENABLED"],
    "keys": self.settings_general["DEV"][".KEYS"],
    "url": self.settings_general["DEV"][".URL"]
}