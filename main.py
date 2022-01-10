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

from selenium.webdriver.chrome import options
try:
    import pyautogui, keyboard

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    from modules.settings import ApplicationSettingsLoader
    from modules.register import ApplicationRegister

except ImportError as err:
    errors.append(err)

class S2SLauncher:
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
                "enabled": item["enabled"],
                "position-x": item["position"][0],
                "position-y": item["position"][1],
                "size-enabled": item["size"]["enabled"],
                "size-value-1": item["size"]["value"][0],
                "size-value-2": item["size"]["value"][1]
            }
        
        self.URL = self.settings["properties"]["URL"]
        self.DIR = self.settings["properties"]["DIR"]
        
        self.combination = self.settings["system"]["combination"]
        self.timer = self.settings["system"]["timer"]

        self.BLOCKED = self.settings["blocked"]

        """ ... """
        os.system("taskkill /F /IM chrome* /T >nul 2>&1")
        time.sleep(self.timer)

        """ ... """
        self.threads = list()

        """ ... """
        combination_t = threading.Thread(target=self.combination)
        combination_t.start()

        """ ... """
        self.register.write(["DEBUG", f"inicializando, para encerrar a aplicação pressione ({self.combination})"])

        self.setup(None)
        
    def combination(self):
        while True:
            command = keyboard.is_pressed(f"{self.combination}")
            if command:
                self.force = False
                for i in self.monitors_dict.values():
                    if i["driver"] != None:
                       self.register.write(["DEBUG", f"({i['name']}): closing..."])
                    
                       i["driver"].quit()

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
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    attempts = 0

                    driver = self.monitors[name]["driver"]

                    driver.get(self.URL)

                    self.commands()

                    driver.execute_script(f'document.title = "monitor {name}"')

                    while True:
                        for blocked in self.BLOCKED:
                            if driver.current_url == blocked or not driver.current_url == self.URL:
                                attempts += 1

                                self.register.write(["WARNING", f"ULR inválida está sendo executada ({driver.current_url}) , número de tentativas: ({attempts})"])

                                driver.get(self.URL)
                            
                                self.commands()

                                driver.execute_script(f'document.title = "monitor {name}"')

                            if attempts > 2:
                                self.register.write(["WARNING", f"após ({3}) tentativas a aplicação não conseguiu resumir o conteúdo, a thread será reiniciada."])

                        if keyboard.is_pressed("alt+p"):
                            driver.get("chrome://whats-new/?auto=true")
                        
                    ### self.monitors[name]["PID"] = self.monitors[name]["driver"].service.process.pid

        except:
            pass


    def setup(self, this):
        if this != None:
            print("")
        else:
            print("S")
        for monitor in self.monitors.values():
            if monitor["enabled"]: 
                driver = webdriver.ChromeOptions()

                ### ...
                driver.add_experimental_option("useAutomationExtension", False)
                driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

                ### ...
                driver.add_argument(f"--user-data-dir={self.DIR}{monitor['name']}")
                driver.add_argument(f"--window-position={monitor['position-x']},{monitor['position-y']}")

                driver.add_argument("--test-type")
                driver.add_argument("--new-window")
                driver.add_argument("--unlimited-storage")
                driver.add_argument("--autoplay-policy=no-user-gesture-required")
                driver.add_argument("--start-fullscreen")
                driver.add_argument("--kiosk")
                driver.add_argument("--disable-notifications")
                driver.add_argument("--disable-extensions")
                driver.add_argument("--disable-infobars")
                driver.add_argument('--disable-blink-features=AutomationControlled')

                monitor["driver"] = webdriver.Chrome(options=driver)

                thread = threading.Thread(name=f"{monitor['name']}", target=self.manager, args=(monitor["name"])).start()
                
                monitor["thread"] = thread

            else:
                self.register.write(["WARNING", f"{monitor['name']} desabilitado!"])

if __name__ == "__main__":
    application = S2SLauncher()
