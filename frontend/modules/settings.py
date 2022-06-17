"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

modules > settings.py | v2 |
"""

import json

def ApplicationSettings():
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
