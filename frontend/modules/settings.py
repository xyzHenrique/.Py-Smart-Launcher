"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

modules > settings.py | v2 |
"""

import json

def ApplicationSettings():
    try:
        data_settings = json.load(open("./system/settings.json"))
        data_monitors = json.load(open(f"./system/presets/{data_settings['MONITORS']['.PRESET']}/preset.json"))

        return data_settings, data_monitors
    except Exception as err:
        print(err)
