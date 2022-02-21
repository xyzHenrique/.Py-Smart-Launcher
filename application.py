# ----------------------------------------------------------------------------------------------
# Created by: Henrique R. Pereira <https://github.com/RIick-013>
# ----------------------------------------------------------------------------------------------

application_version = "3.6.2"

try:
    import os,  time, threading, pyautogui, keyboard

    from selenium import webdriver

    from modules.settings import ApplicationSettingsLoader
    from modules.logger import ApplicationLogger
    from update import ApplicationUpdate

except ImportError as err:
    print(err)

class Application:
    def __init__(self):
        self.logger = ApplicationLogger()
        self.system_settings = ApplicationSettingsLoader()[0]
        self.system_monitors = ApplicationSettingsLoader()[1]
        
        """MONITORS"""
        self.monitors = dict() 

        for key,item in self.system_monitors["monitors"].items():
            self.monitors[key] = {
                "PID": None,
                "NAME": key,
                "DRIVER": None,
                "THREAD": None,

                "monitor-enabled": item["monitor"]["enabled"],
                "monitor-position-x": item["monitor"]["x"],
                "monitor-position-y": item["monitor"]["y"],
                
                "size-enabled": item["size"]["enabled"],
                "size-x": item["size"]["x"],
                "size-y": item["size"]["y"],
                
                "DIR": item["DIR"]
            }
    
        """SETTINGS.APPLICATION"""
        self.settings_application = self.system_settings["APPLICATION"]

        """SETTINGS.BLOCK"""
        self.settings_block = self.system_settings["BLOCK"]
        
        """SETTINGS.SYSTEM"""
        self.settings_system_force_url = self.system_settings["SYSTEM"][".FORCE-URL"]
        self.settings_system_secure_exit = self.system_settings["SYSTEM"][".SECURE-EXIT"]
        self.settings_system_secure_start = self.system_settings["SYSTEM"][".SECURE-START"]

        self.settings_system_secure_restart = {
            "enabled": self.system_settings["SYSTEM"][".SECURE-RESTART"][0],
            "attempts": self.system_settings["SYSTEM"][".SECURE-RESTART"][1]
            }
        
        self.settings_system_datetime = {
            "enabled": self.system_settings["SYSTEM"][".DATETIME"][0], 
            "url": self.system_settings["SYSTEM"][".DATETIME"][1], 
            "ssl": self.system_settings["SYSTEM"][".DATETIME"][2]
            }
        
        self.settings_system_laumcher_mode = "normal"
        
        """SETTINGS.AUTOMATION"""
        self.settings_automation = {
            "enabled": self.system_settings["AUTOMATION"][".ENABLED"], 
            "keys": self.system_settings["AUTOMATION"][".KEYS"]
            }

        """SETTINGS.DEV"""
        self.settings_dev = {
            "enabled": self.system_settings["DEV"][".ENABLED"],
            "key": self.system_settings["DEV"][".KEY"],
            "url": self.system_settings["DEV"][".URL"]
        }

        
        if self.settings["system"]["clear-start"]:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

        exit_t = threading.Thread(target=self.exit_command)
        exit_t.start()

        
        self.register.write(["DEBUG", f"S2SLauncher\n- versão da aplicação: {} - Criado por: ({self.exit_keys})"])
    
        #self.setup()
    
    def secure_start(self):
        if self.settings_system_secure_start:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

    def exit_command(self):
        while True: 
            if keyboard.is_pressed(f"{self.exit_keys}"):
                self.register.write(["INFO", f"finalizando, por favor aguarde..."])

                os.system("taskkill /F /IM chrome* /T >nul 2>&1")           

    def restart(self):
        try: 
            self.register.write(["CRITICAL", f"reiniciando aplicação...\n"])

            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

            time.sleep(1.5)

            path = os.getcwd()
            
            if os.path.isfile(f"{path}/S2SLauncher.exe"):
                os.system(f"start {path}\S2SLauncher.exe")
            else:
                os.system(f"start {path}\main.py")

            os._exit(0)

        except Exception as err:
            self.register.write(["ERROR", f"{err}"])
            
            os._exit(0)
    
    def auto_keyboard_commands(self):
        if self.auto_keyboard_enabled:
            try:
                for key in self.auto_keyboard_keys:
                    pyautogui.press(key)

                    ### print(f"'{key}' pressed!")

                    time.sleep(0.3)

            except Exception as err:
                self.register.write(["ERROR", f"{err}"])

    def manager(self, name):
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    attempts = 0

                    driver = self.monitors[name]["DRIVER"]
                    PID = driver.service.process.pid

                    driver.get(self.URL)

                    self.auto_keyboard_commands()

                    driver.execute_script(f'document.title = "monitor {name}"')

                    self.register.write(["INFO", f"monitor {self.monitors[name]['name']} ({PID}) criado com sucesso!"])

                    while True:
                        for blocked in self.blocked:
                            if driver.current_url == blocked or not driver.current_url == self.URL:
                                attempts += 1

                                self.register.write(["WARNING", f"uma ULR inválida está sendo executada no monitor {name} - ({driver.current_url}), número de tentativas: ({attempts})"])

                                driver.get(self.URL)
                            
                                self.auto_keyboard_commands()

                                driver.execute_script(f'document.title = "monitor {name}"')
                            
                            if attempts >= self.fix_attempts:
                                self.register.write(["WARNING", f"o número máximo de tentativas foi atingido ({attempts})!"])
                                    
                                driver.quit()

                                break

                        if self.simulate_test_enabled:
                            driver.execute_script(f'document.title = "simulate test - monitor {name}"')

                            if keyboard.is_pressed(self.simulate_test_key):
                                driver.get(self.simulate_test_url)

                        time.sleep(1.5)
        except Exception as err:
            self.register.write(["WARNING", f"monitor {self.monitors[name]['name']} ({err})"])

            self.restart()
        
    def setup(self):
        try:
            for monitor in self.monitors.values():
                if monitor["monitor-enabled"]: 
                    driver = webdriver.ChromeOptions(executable_path="./driver/chromedriver.exe")

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
            
                    thread = threading.Thread(target=self.manager, args=(monitor["name"]))
                    
                    monitor["thread"] = thread
                    
                    time.sleep(0.3)

                    thread.start()
                else:
                    self.register.write(["WARNING", f"monitor {monitor['name']} está desabilitado!"])
        
        except Exception as err:
            self.register.write(["CRITICAL", f"{err}"])

            self.restart()

if __name__ == "__main__":
    application = ApplicationTray()
