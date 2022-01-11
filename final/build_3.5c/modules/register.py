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
# register.py > module script
#
# v3.5
# ----------------------------------------------------------------------------------------------

import datetime, time, os

### LEVELS: INFO, WARNING, ERROR, CRITICAL and DEBUG

class ApplicationRegister:
    def __init__(self):
        self.now = [datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S")]
        
        self.logname = self.now[0].replace("/", "-")

        self.levels = ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]

        self.logs_path = "./system/logs/"

    def setup(self):
            exist = False

            if os.path.exists(f"{self.logs_path}{self.logname}.txt"):
                exist = True
            else:
                try:
                    f = open(f"{self.logs_path}{self.logname}.txt", "w+")
                    
                    time.sleep(0.5)

                    self.write(["DEBUG", f"arquivo ({self.logname}.txt) criado com sucesso!\n"])
                    
                    exist = True
                except:
                    print(f"[{self.now[0]} | {self.now[1]}] - ERROR - não foi possível criar o arquivo (logs/{self.logname}.txt)!")

                    exist = False

            return exist

    def write(self, msg):
        if self.setup():
            f = open(f"{self.logs_path}{self.logname}.txt", "a")
            
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
