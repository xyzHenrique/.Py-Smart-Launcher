# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------
# Wide Digital - S2S launcher python automation
#
# ~ ----------------------------- LINKS ----------------------------- ~
# chromedriver: <https://chromedriver.chromium.org/downloads>
# selenium: <https://selenium-python.readthedocs.io/api.html>
# pyautogui: <https://pyautogui.readthedocs.io/en/latest/>
# ~ ----------------------------------------------------------------- ~
#
# Created by: Henrique R. Pereira <https://github.com/RIick-013>
#
# S2SSettings.py > module script
#
# v3.0
# ----------------------------------------------------------------------------------------------

import json

def settingsloader():
    try:
        data = json.load(open("settings.json"))

        return data
    except Exception as err:
        print(err)
