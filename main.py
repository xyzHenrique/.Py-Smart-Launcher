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
    from selenium.webdriver.chrome.options import Options

    from modules.settings import ApplicationSettingsLoader
    from modules.register import ApplicationRegister

except ImportError as err:
    errors.append(err)

class S2SLauncher:
    def __init__(self):
        ### os.system("taskkill /F /IM chrome* /T >nul 2>&1")

        self.register = ApplicationRegister()
        self.settings = ApplicationSettingsLoader()
        
        """ SETTINGS MONITORS """
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

        """ SETTINGS SYSTEM """
        self.combination = self.settings["system"]["combination"]

        """ ... """
        self.threads = list()

        """ ... """
        #command_thread = threading.Thread(target=self.combination_command)
        #command_thread.start()

        """ ...  """
        ### self.logger.write(["DEBUG", f"initializing monitors please wait, to exit press keys combination: [ {self.combination} ]"])

        self.monitors_setup()
        
    def combination_command(self):
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
       
    def monitors_autocommands(self, driver, name):
        """ AUTO COMMANDS """
        pyautogui.press("f5")
        time.sleep(0.5)
        
        driver.get(self.URL)
        time.sleep(0.5)
        
        driver.execute_script(f'document.title = "S2S - {name}"')
        
        pyautogui.press("esc")
            
    def monitor_1(self):
        """ MANAGER MONITOR 1 """
        mydriver, myname, mypid = self.monitors_dict["monitor-1"]["driver"], self.monitors_dict["monitor-1"]["name"], self.monitors_dict["monitor-1"]["PID"]

        self.logger.write(["INFO", f"({myname}): started with PID ({mypid})"])

        self.monitors_autocommands(mydriver, myname)

        while True:
            try:
                time.sleep(0.5)

                if mydriver.current_url == self.URL:
                    pass
                else:
                    self.logger.write(["WARNING", f"({myname}): invalid URL ({mydriver.current_url})"])
                    break

            except Exception as err: 
                self.logger.write(["CRITICAL", f"({myname}): ERROR [{err}]"])
                break

        self.restart()

    def monitor_2(self):
        """ MANAGER MONITOR 2 """
        mydriver, myname, mypid = self.monitors_dict["monitor-2"]["driver"], self.monitors_dict["monitor-2"]["name"], self.monitors_dict["monitor-2"]["PID"]

        self.logger.write(["INFO", f"({myname}): started with PID ({mypid})"])

        self.monitors_autocommands(mydriver, myname)
        
        while True:
            try:
                time.sleep(0.5)

                if mydriver.current_url == self.URL:
                    pass
                else:
                    self.logger.write(["WARNING", f"({myname}): invalid URL ({mydriver.current_url})"])
                    break

            except Exception as err: 
                self.logger.write(["CRITICAL", f"({myname}): ERROR [{err}]"])
                break

        self.restart()

    def monitor_3(self):
        """ MANAGER MONITOR 3 """
        mydriver, myname, mypid = self.monitors_dict["monitor-3"]["driver"], self.monitors_dict["monitor-3"]["name"], self.monitors_dict["monitor-3"]["PID"]

        self.logger.write(["INFO", f"({myname}): started with PID ({mypid})"])

        self.monitors_autocommands(mydriver, myname)
        
        while True:
            try:
                time.sleep(0.5)

                if mydriver.current_url == self.URL:
                    pass
                else:
                    self.logger.write(["WARNING", f"({myname}): invalid URL ({mydriver.current_url})"])
                    break

            except Exception as err: 
                self.logger.write(["CRITICAL", f"({myname}): ERROR [{err}]"])
                break

        self.restart()

    def monitor_4(self):
        """ MANAGER MONITOR 4 """
        mydriver, myname, mypid = self.monitors_dict["monitor-4"]["driver"], self.monitors_dict["monitor-4"]["name"], self.monitors_dict["monitor-4"]["PID"]

        self.logger.write(["INFO", f"({myname}): started with PID ({mypid})"])

        self.monitors_autocommands(mydriver, myname)
        
        while True:
            try:
                time.sleep(0.5)

                if mydriver.current_url == self.URL:
                    pass
                else:
                    self.logger.write(["WARNING", f"({myname}): invalid URL ({mydriver.current_url})"])
                    break

            except Exception as err: 
                self.logger.write(["CRITICAL", f"({myname}): ERROR [{err}]"])
                break

        self.restart()

    def monitors_manager(self, name):
        for monitor in self.monitors.keys():
            if name == monitor:
                self.monitors[name]["PID"] = self.monitors[name]["driver"].service.process.pid

                print(self.monitrs[name]["PID"])


    def monitors_setup(self):
        """ SETUP FOR WEBDRIVER """
        for monitor in self.monitors.values():
            ### ...
            monitor["driver"] = webdriver.ChromeOptions()

            ### ...
            monitor["driver"].add_experimental_option("useAutomationExtension", False)
            monitor["driver"].add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

            ### ...
            monitor["driver"].add_argument(f"--user-data-dir={self.DIR}{monitor['name']}")
            monitor["driver"].add_argument(f"--window-position={monitor['position-x']},{monitor['position-y']}")
        
            ### ...
            monitor["driver"].add_argument("--test-type")
            monitor["driver"].add_argument("--new-window")
            monitor["driver"].add_argument("--unlimited-storage")
            monitor["driver"].add_argument("--autoplay-policy=no-user-gesture-required")
            monitor["driver"].add_argument("--start-fullscreen")
            monitor["driver"].add_argument("--kiosk")
            monitor["driver"].add_argument("--disable-notifications")
            monitor["driver"].add_argument("--disable-extensions")
            monitor["driver"].add_argument("--disable-infobars")

            ### ...
            if monitor["enabled"]: 
                ### print(f"{monitor['name']} enabled!")
                
                t = threading.Thread(name=f"{monitor['name']}", target=self.monitors_manager, args=(monitor["name"]))
                self.threads.append(t)
                t.start()

            else:
                print(f"{monitor['name']} disabled!")
                ### self.logger.write(["WARNING", f"{self.monitors_dict['monitor-1']['name']}: disabled!"])

if __name__ == "__main__":
    application = S2SLauncher()
