# ----------------------------------------------------------------------------------------------
# Created by: Henrique R. Pereira <https://github.com/RIick-013>
#
# ~ ----------------------------- LINKS ----------------------------- ~
# https://chromedriver.chromium.org/downloads
# https://selenium-python.readthedocs.io/api.html
# https://pyautogui.readthedocs.io/en/latest/
# ~ ----------------------------------------------------------------- ~
#
# settings.py > module script
#
# v3.6
# ----------------------------------------------------------------------------------------------

import json

def ApplicationSettings():
    try:
        data_settings = json.load(open("./system/settings.json"))
        data_monitors = json.load(open("./system/monitors.json"))

        return data_settings, data_monitors
    except Exception as err:
        print(err)
