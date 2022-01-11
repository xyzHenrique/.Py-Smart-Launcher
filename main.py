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
# main.py main script
#
# v3.5c
# ----------------------------------------------------------------------------------------------

import sys, os, time, threading

try:
    import pyautogui, keyboard, glob

    ### ...
    from selenium import webdriver
    
    ### ...
    from PIL import ImageGrab
    from functools import partial

    ### ...
    from modules.settings import ApplicationSettingsLoader
    from modules.register import ApplicationRegister

except ImportError as err:
    print(err)

    time.sleep(5.0)

class Launcher:
    def __init__(self):
        self.register = ApplicationRegister()
        self.settings = ApplicationSettingsLoader()
        
        """ SETTINGS """
        self.monitors = dict() 
            
        for key,item in self.settings["properties"]["monitors"].items():
            self.monitors[key] = {
                "driver": None,
                "PID": None,
                "thread": None,
                "name": f"{key}",

                "monitor-enabled": item["monitor-enabled"],
                "monitor-position-x": item["monitor-position-xy"][0],
                "monitor-position-y": item["monitor-position-xy"][1],
                
                "monitor-size-enabled": item["monitor-size"]["monitor-size-enabled"],
                "monitor-size-x": item["monitor-size"]["monitor-size-xy"][0],
                "monitor-size-y": item["monitor-size"]["monitor-size-xy"][1],
                
                "DIR": item["DIR"]
            }
        
        ### ...
        self.URL = self.settings["properties"]["application-URL"]
        
        ### ...
        self.keys_combination = self.settings["system"]["keys-combination"]
        self.fix_attempts = self.settings["system"]["fix-attempts"]

        self.start_cleaning = self.settings["system"]["start-cleaning"]
        
        ### ...
        self.auto_click_enabled = self.settings["automation"]["auto_click_enabled"]

        self.auto_keyboard_enabled = self.settings["automation"]["auto_keyboard_enabled"]
        self.auto_keyboard_keys = self.settings["automation"]["auto_keyboard_keys"]

        ### ...
        self.blocked = self.settings["blocked-URL"]

        ### ...
        self.simulate_test_enabled = self.settings["simulate-test"]["enabled"]
        self.simulate_test_key = self.settings["simulate-test"]["key"]
        self.simulate_test_url = self.settings["simulate-test"]["URL"]

        ### ...
        if self.start_cleaning:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

        """ ... """
        combination_t = threading.Thread(target=self.combination_command)
        combination_t.start()

        """ ... """
        self.register.write(["DEBUG", f"inicializando, para finalizar a aplicação corretamente pressione ({self.keys_combination})"])

        self.setup()
        
    def combination_command(self):
        while True:
            command = keyboard.is_pressed(f"{self.keys_combination}")
            if command:
                for monitor in self.monitors.values():
                    if monitor["driver"] != None:
                       
                       self.register.write(["INFO", f"encerrando o monitor {monitor['name']}, por favor aguarde..."])
                    
                       monitor["driver"].quit()
                       monitor["thread"].join()

                sys.exit()                

    def restart(self):
        try: 
            for monitor in self.monitors.values():
                if monitor["driver"] != None:
                    
                    self.register.write(["WARNING", f"finalizando o monitor {monitor['name']}, por favor aguarde..."])
                
                    monitor["driver"].quit()
                    monitor["thread"].join()

            self.register.write(["CRITICAL", f"reiniciando aplicação...\n"])

            time.sleep(2.5)

            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
        
        except Exception as err:
            self.register.write(["ERROR", f"{err}"])
            
            sys.exit()
    
    def auto_click_commands(self):
        if self.auto_click_enabled:
            try:
                ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

                for img in glob.glob("./system/images/minidb/*.png"):
                    item = pyautogui.locateOnScreen(img)

                    if item:
                        self.register.write(["INFO", f"AUTO-CLICK-MODULE: '{item}' click!"])

                        pyautogui.moveTo(item)
                        pyautogui.click()
                        
                    else:
                        pass
            except Exception as err:
                self.register.write(["ERROR", f"AUTO-CLICK-MODULE: {err}"])

    def auto_keyboard_commands(self):
        if self.auto_keyboard_enabled:
            try:
                for key in self.auto_keyboard_keys:
                    pyautogui.press(key)

                    self.register.write(["INFO", f"AUTO-KEYBOARD-MODULE: '{key}' pressed!"])

                    time.sleep(0.3)

            except Exception as err:
                self.register.write(["ERROR", f"AUTO-KEYBOARD-MODULE: {err}"])

    def manager(self, name):
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    attempts = 0

                    driver = self.monitors[name]["driver"]
                    PID = driver.service.process.pid

                    driver.get(self.URL)

                    self.auto_keyboard_commands()

                    driver.execute_script(f'document.title = "monitor {name}"')

                    self.register.write(["INFO", f"monitor {self.monitors[name]['name']} ({PID}) criado com sucesso!"])

                    while True:
                        
                        self.auto_click_commands()
                       
                        for blocked in self.blocked:
                            if driver.current_url == blocked or not driver.current_url == self.URL:
                                attempts += 1

                                self.register.write(["WARNING", f"uma ULR inválida está sendo executada ({driver.current_url}), número de tentativas: ({attempts})"])

                                driver.get(self.URL)
                            
                                self.auto_keyboard_commands()

                                driver.execute_script(f'document.title = "monitor {name}"')

                            if attempts >= self.fix_attempts:
                                self.register.write(["WARNING", f"o número máximo de tentativas foi atingido ({attempts}), o monitor {name} será reiniciado!"])
                                    
                                driver.quit()

                                self.restart()

                        if self.simulate_test_enabled:
                            driver.execute_script(f'document.title = "(! SIMULATE TEST !) - monitor {name}"')

                            if keyboard.is_pressed(self.simulate_test_key):
                                driver.get(self.simulate_test_url)

        except Exception as err:
            self.register.write(["DEBUG", f"monitor {self.monitors[name]['name']} finalizado! ({err})"])

            self.restart()
        
    def setup(self):
        try:
            for monitor in self.monitors.values():
                if monitor["monitor-enabled"]: 
                    driver = webdriver.ChromeOptions()

                    ### ...
                    driver.add_experimental_option("useAutomationExtension", False)
                    driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

                    ### ...
                    driver.add_argument(f"--user-data-dir={monitor['DIR']}")
                    driver.add_argument(f"--window-position={monitor['monitor-position-x']},{monitor['monitor-position-y']}")

                    ### ...
                    if monitor["monitor-size-enabled"]:
                        driver.add_argument(f"--app={self.URL}")
                        driver.add_argument(f"--window-size={monitor['monitor-size-x']},{monitor['monitor-size-y']}")
                    else:
                        ### driver.add_argument("--start-fullscreen") ###
                        driver.add_argument("--kiosk")
                    
                    ### ...
                    driver.add_argument("--test-type")
                    driver.add_argument("--new-window")
                    driver.add_argument("--unlimited-storage")
                    driver.add_argument("--disable-extensions")                
                    driver.add_argument("--disable-notifications")
                    driver.add_argument("--ignore-certificate-errors")
                    driver.add_argument("--autoplay-policy=no-user-gesture-required")
                
                    monitor["driver"] = webdriver.Chrome(options=driver)

                    self.register.write(["INFO", f"argumentos adicionadas ao monitor {monitor['name']}"])
            
                    thread = threading.Thread(target=self.manager, args=(monitor["name"]))
                    
                    monitor["thread"] = thread
                    
                    thread.start()
                else:
                    self.register.write(["WARNING", f"monitor {monitor['name']} está desabilitado!"])
        
        except Exception as err:
            self.register.write(["CRITICAL", f"{err}"])

            self.restart()

if __name__ == "__main__":
    application = Launcher()
