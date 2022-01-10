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
# S2SLauncher.py main script
#
# v3.5
# ----------------------------------------------------------------------------------------------

errors = []

import sys, os, time, threading

try:
    import pyautogui, keyboard

    from selenium import webdriver

    from PIL import ImageGrab
    import glob
    from functools import partial

    from modules.settings import ApplicationSettingsLoader
    from modules.register import ApplicationRegister

except ImportError as err:
    print(err)

class Launcher:
    def __init__(self):
        self.register = ApplicationRegister()
        self.settings = ApplicationSettingsLoader()
        
        """ ... """
        self.monitors = dict() 
            
        for key,item in self.settings["properties"]["monitors"].items():
            self.monitors[key] = {
                "driver": None,
                "PID": None,
                "thread": None,
                "name": f"{key}",

                "monitor-enabled": item["enabled"],
                "monitor-position-x": item["xy"][0],
                "monitor-position-y": item["xy"][1],
                "monitor-size": item["size"]["enabled"],
                "monitor-size-x": item["size"]["xy"][0],
                "monitor-size-y": item["size"]["xy"][1],
                "DIR": item["DIR"]
            }
        
        self.URL = self.settings["properties"]["URL"]
        
        self.combination = self.settings["system"]["combination"]
        self.timer = self.settings["system"]["timer"]
        self.attempts = self.settings["system"]["attempts"]

        self.BLOCKED = self.settings["blocked"]

        """ ... """
        os.system("taskkill /F /IM chrome* /T >nul 2>&1")
        time.sleep(self.timer)

        """ ... """
        combination_t = threading.Thread(target=self.combination_command)
        combination_t.start()

        """ ... """
        self.register.write(["DEBUG", f"inicializando, para encerrar a aplicação corretamente pressione ({self.combination})"])

        self.setup()
        
    def combination_command(self):
        while True:
            command = keyboard.is_pressed(f"{self.combination}")
            if command:
                for monitor in self.monitors.values():
                    if monitor["driver"] != None:
                       
                       self.register.write(["DEBUG", f"encerrando monitor {monitor['name']}, por favor aguarde..."])
                    
                       monitor["driver"].quit()
                       monitor["thread"].join()

                sys.exit()                


    def restart(self):
        if self.force == True:
            try: 
                self.logger.write(["CRITICAL", f"restarting...\n\n"])

                time.sleep(2.5)

                os.execv(sys.executable, ["python"] + sys.argv)    
            except Exception as err:
                self.logger.write(["ERROR", f"{err}"])
                quit()
       
    def commands(self):
        pyautogui.press("f5")
        
        time.sleep(0.3)
        
        pyautogui.press("esc")
            
    def manager(self, name):
        PID = None
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    
                    attempts = 0

                    driver = self.monitors[name]["driver"]
                    PID = driver.service.process.pid

                    driver.get(self.URL)

                    self.commands()

                    driver.execute_script(f'document.title = "monitor {name}"')

                    self.register.write(["INFO", f"monitor {self.monitors[name]['name']} ({PID}) criado com sucesso!"])
                    
                    while True:
                        
                        for blocked in self.BLOCKED:
                            if driver.current_url == blocked or not driver.current_url == self.URL:
                                attempts += 1

                                self.register.write(["WARNING", f"uma ULR inválida está sendo executada ({driver.current_url}), número de tentativas: ({attempts})"])

                                driver.get(self.URL)
                            
                                self.commands()

                                driver.execute_script(f'document.title = "monitor {name}"')

                            if attempts >= 1:
                                self.register.write(["WARNING", f"o número máximo de tentativas foi atingido ({attempts}), o monitor {name} será reiniciado!"])
                                    
                                driver.quit()

                                sys.exit()

                        if keyboard.is_pressed("p"):
                            driver.get("chrome://whats-new/?auto=true")        
        except Exception as err:
            os.system(f"taskkill /F /PID {PID} /T >nul 2>&1")

            self.register.write(["DEBUG", f"monitor {self.monitors[name]['name']} encerrado! ({err})"])
        
    def setup(self):
        for monitor in self.monitors.values():
            if monitor["enabled"]: 
                driver = webdriver.ChromeOptions()

                """ ... """
                driver.add_experimental_option("useAutomationExtension", False)
                driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

                """ ... """
                driver.add_argument(f"--user-data-dir={self.DIR}{monitor['name']}")
                driver.add_argument(f"--window-position={monitor['position-x']},{monitor['position-y']}")

                driver.add_argument("--window-size=2560,750")
                

                """ ... """
                driver.add_argument("--test-type")
                driver.add_argument("--new-window")
                driver.add_argument("--unlimited-storage")
                driver.add_argument("--autoplay-policy=no-user-gesture-required")
                #driver.add_argument("--start-fullscreen")
                #driver.add_argument("--kiosk")
                driver.add_argument("--disable-notifications")
                driver.add_argument("--disable-extensions")
                driver.add_argument('--ignore-certificate-errors')
            
                monitor["driver"] = webdriver.Chrome(options=driver)

                self.register.write(["INFO", f"argumentos adicionadas ao monitor {monitor['name']}"])
        
                thread = threading.Thread(target=self.manager, args=(monitor["name"]))
                
                monitor["thread"] = thread
                
                thread.start()
            else:
                self.register.write(["WARNING", f"monitor {monitor['name']} está desabilitado!"])

if __name__ == "__main__":
    application = Launcher()
