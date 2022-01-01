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
# v3.0
# ----------------------------------------------------------------------------------------------

errors = []

import sys, os, time, threading
try:
    import pyautogui, keyboard

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    from S2SSettings import settingsloader
    from S2SLogger import S2SLogger

except ImportError as err:
    errors.append(err)

class S2SLauncher:
    def __init__(self):
        os.system("taskkill /F /IM chrome* /T >nul 2>&1")

        if errors:
            i = 0
            for e in errors:
                i += 1
                print(f"TOTAL: ({i}) - ERROR: ({e})\n") 
                time.sleep(10.0)
            self.restart()

        self.logger = S2SLogger()

        """ SETTINGS """
        self.settings = settingsloader()

        ### --- monitors settings
        self.monitor_1_settings = {
                                   "enabled": self.settings["monitors"]["monitor-1"]["enabled"],
                                   "coordsx": self.settings["monitors"]["monitor-1"]["coordsx"],
                                   "coordsy": self.settings["monitors"]["monitor-1"]["coordsy"],
                                   "DIR": self.settings["monitors"]["monitor-1"]["DIR"]
                                   }

        self.monitor_2_settings = {
                                   "enabled": self.settings["monitors"]["monitor-2"]["enabled"],
                                   "coordsx": self.settings["monitors"]["monitor-2"]["coordsx"],
                                   "coordsy": self.settings["monitors"]["monitor-2"]["coordsy"],
                                   "DIR": self.settings["monitors"]["monitor-2"]["DIR"]
                                   }

        self.monitor_3_settings = {
                                   "enabled": self.settings["monitors"]["monitor-3"]["enabled"],
                                   "coordsx": self.settings["monitors"]["monitor-3"]["coordsx"],
                                   "coordsy": self.settings["monitors"]["monitor-3"]["coordsy"],
                                   "DIR": self.settings["monitors"]["monitor-3"]["DIR"]
                                   }

        self.monitor_4_settings = {
                                   "enabled": self.settings["monitors"]["monitor-4"]["enabled"],
                                   "coordsx": self.settings["monitors"]["monitor-4"]["coordsx"],
                                   "coordsy": self.settings["monitors"]["monitor-4"]["coordsy"],
                                   "DIR": self.settings["monitors"]["monitor-4"]["DIR"]
                                   }

        """ DICTS """
        self.monitors_dict = {
                              "monitor-1": {"driver": None, "name": "monitor-1", "thread": None, "PID": None},
                              "monitor-2": {"driver": None, "name": "monitor-2", "thread": None, "PID": None},
                              "monitor-3": {"driver": None, "name": "monitor-3", "thread": None, "PID": None},
                              "monitor-4": {"driver": None, "name": "monitor-4", "thread": None, "PID": None}
                             }

        """ LISTS """   
        self.threads = list()

        """ VARIABLES """
        self.URL = "https://s2s.widedigital.com.br/S2S/Player.html"

        """ THREAD INTERNAL """
        self.combination = "ctrl+alt+p"

        self.force = True

        internal_thread = threading.Thread(target=self.exit_command)
        internal_thread.start()

        """ FUNCTIONS """
        self.logger.write(["DEBUG", f"initializing monitors please wait, to exit press keys combination: [ {self.combination} ]"])

        self.monitors_setup()
        
    def exit_command(self):
        while True:
            command = keyboard.is_pressed(f"{self.combination}")
            if command:
                self.force = False
                for i in self.monitors_dict.values():
                    if i["driver"] != None:
                       self.logger.write(["DEBUG", f"({i['name']}): closing..."])
                    
                       i["driver"].quit()

                self.logger.write(["DEBUG", f"finishing, please wait..."])
                sys.exit()
 
    def restart(self):
        if self.force == True:
            try: 
                self.logger.write(["CRITICAL", f"restarting...\n\n\n"])

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

    def monitors_setup(self):
        """ SETUP FOR WEBDRIVER """
        # ----------------------------------------------------------------------------------------------
        self.m1_options, self.m2_options, self.m3_options, self.m4_options = webdriver.ChromeOptions(), webdriver.ChromeOptions(), webdriver.ChromeOptions(), webdriver.ChromeOptions()
        
        for driver in [self.m1_options, self.m2_options, self.m3_options, self.m4_options]:
            #--- disable the automation banners and logging messages ---#
            driver.add_experimental_option("useAutomationExtension", False)
            driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

            ### options for webdriver monitor 1
            if driver == self.m1_options:
                driver.add_argument("--user-data-dir={}".format(self.monitor_1_settings['DIR']))
                driver.add_argument("--window-position={},{}".format(self.monitor_1_settings['coordsx'], self.monitor_1_settings['coordsy']))
            
            ### options for webdriver monitor 2
            if driver == self.m2_options:
                driver.add_argument("--user-data-dir={}".format(self.monitor_2_settings['DIR']))
                driver.add_argument("--window-position={},{}".format(self.monitor_2_settings['coordsx'], self.monitor_2_settings['coordsy']))
            
            ### options for webdriver monitor 3
            if driver == self.m3_options:
                driver.add_argument("--user-data-dir={}".format(self.monitor_3_settings['DIR']))
                driver.add_argument("--window-position={},{}".format(self.monitor_3_settings['coordsx'], self.monitor_3_settings['coordsy']))
            
            ### options for webdriver monitor 4
            if driver == self.m4_options:
                driver.add_argument("--user-data-dir={}".format(self.monitor_4_settings['DIR']))
                driver.add_argument("--window-position={},{}".format(self.monitor_4_settings['coordsx'], self.monitor_4_settings['coordsy']))

            ### options for all webdriver monitors
            driver.add_argument("--test-type")
            driver.add_argument("--new-window")
            driver.add_argument("--unlimited-storage")
            driver.add_argument("--autoplay-policy=no-user-gesture-required")
            driver.add_argument("--start-fullscreen")
            driver.add_argument("--kiosk")
            driver.add_argument("--disable-notifications")
            driver.add_argument("--disable-extensions")
            driver.add_argument("--disable-infobars")

        # ----------------------------------------------------------------------------------------------
        m1_t, m2_t, m3_t, m4_t = None, None, None, None

        ### monitor-1 thread and config
        if self.monitor_1_settings["enabled"]: 
            self.monitors_dict["monitor-1"]["driver"] = webdriver.Chrome(options=self.m1_options,)
            self.monitors_dict["monitor-1"]["PID"] = self.monitors_dict["monitor-1"]["driver"].service.process.pid

            m1_t = threading.Thread(name=f"thread-{self.monitors_dict['monitor-1']['name']}", target=self.monitor_1)
            m1_t.start()

            self.monitors_dict["monitor-1"]["thread"] = m1_t

        else:
            self.logger.write(["WARNING", f"{self.monitors_dict['monitor-1']['name']}: disabled!"])

        ### monitor-2 thread and config
        if self.monitor_2_settings["enabled"]: 
            self.monitors_dict["monitor-2"]["driver"] = webdriver.Chrome(options=self.m2_options,)
            self.monitors_dict["monitor-2"]["PID"] = self.monitors_dict["monitor-2"]["driver"].service.process.pid

            m2_t = threading.Thread(name=f"thread-{self.monitors_dict['monitor-2']['name']}", target=self.monitor_2)
            m2_t.start()

            self.monitors_dict["monitor-2"]["thread"] = m2_t

        else:
            self.logger.write(["WARNING", f"{self.monitors_dict['monitor-2']['name']}: disabled!"])

        ### monitor-3 thread and config
        if self.monitor_3_settings["enabled"]: 
            self.monitors_dict["monitor-3"]["driver"] = webdriver.Chrome(options=self.m3_options,)
            self.monitors_dict["monitor-3"]["PID"] = self.monitors_dict["monitor-3"]["driver"].service.process.pid

            m3_t = threading.Thread(name=f"thread-{self.monitors_dict['monitor-3']['name']}", target=self.monitor_3)
            m3_t.start()

            self.monitors_dict["monitor-3"]["thread"] = m3_t

        else:
            self.logger.write(["WARNING", f"{self.monitors_dict['monitor-3']['name']}: disabled!"])

        ### monitor-4 thread and config
        if self.monitor_4_settings["enabled"]: 
            self.monitors_dict["monitor-4"]["driver"] = webdriver.Chrome(options=self.m4_options,)
            self.monitors_dict["monitor-4"]["PID"] = self.monitors_dict["monitor-4"]["driver"].service.process.pid

            m4_t = threading.Thread(name=f"thread-{self.monitors_dict['monitor-4']['name']}", target=self.monitor_4)
            m4_t.start()

            self.monitors_dict["monitor-4"]["thread"] = m4_t

        else:
            self.logger.write(["WARNING", f"{self.monitors_dict['monitor-4']['name']}: disabled!"])

        for thread in [m1_t, m2_t, m3_t, m4_t]:
            self.threads.append(thread)    

if __name__ == "__main__":
    application = S2SLauncher()
