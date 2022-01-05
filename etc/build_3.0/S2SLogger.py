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
# S2SLogger.py > module script
#
# v3.0
# ----------------------------------------------------------------------------------------------

import datetime, time, os

### LEVELS: INFO, WARNING, ERROR, CRITICAL and DEBUG

class S2SLogger:
    def __init__(self):
        self.now = [datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S")]
        
        self.logname = self.now[0].replace("/", "-")

        self.levels = ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]

    def setup(self):
            exist = False

            if os.path.exists(f"logs/{self.logname}.txt"):
                exist = True
            else:
                try:
                    f = open(f"logs/{self.logname}.txt", "w+")
                    
                    time.sleep(0.5)

                    self.write(["DEBUG", f"LOG ({self.logname}.txt) file created and started!\n"])
                    
                    exist = True
                except:
                    print(f"[{self.now[0]} | {self.now[1]}] - ERROR - could not create LOG (logs/{self.logname}.txt) file!")

                    exist = False

            return exist

    def write(self, msg):
        if self.setup():
            f = open(f"logs/{self.logname}.txt", "a")
            
            if msg[0] == self.levels[0]:
                m = f"[{self.now[0]} | {self.now[1]}] - INFO - {msg[1]}\n"
                
                print(m)
                f.write(m)

            if msg[0] == self.levels[1]:
                m = f"[{self.now[0]} | {self.now[1]}] - WARNING - {msg[1]}\n"
                
                print(m)
                f.write(m)

            if msg[0] == self.levels[2]:
                m = f"[{self.now[0]} | {self.now[1]}] - ERROR - {msg[1]}\n"
                
                print(m)
                f.write(m)

            if msg[0] == self.levels[3]:
                m = f"[{self.now[0]} | {self.now[1]}] - CRITICAL - {msg[1]}\n"
                
                print(m)
                f.write(m)

            if msg[0] == self.levels[4]:
                m = f"[{self.now[0]} | {self.now[1]}] - DEBUG - {msg[1]}\n"
        
                print(m)
                f.write(m)

        else:
            self.setup()
