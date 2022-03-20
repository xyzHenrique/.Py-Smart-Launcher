# ----------------------------------------------------------------------------------------------
# Created by: Henrique R. Pereira <https://github.com/RIick-013>
# ----------------------------------------------------------------------------------------------

version = "3.6.5"

try:
    import os, time, threading, pyautogui, keyboard

    from selenium import webdriver

    from modules.settings import ApplicationSettings
    from modules.logger import ApplicationLogger

except ImportError as err:
    print(err)

class Application:
    def __init__(self):
        self.logger = ApplicationLogger()
        self.settings = ApplicationSettings()

        self.settings_general, self.settings_monitors = self.settings[0], self.settings[1]
        
        self.monitors = dict() 
        
        for key,item in self.settings_monitors["MONITORS"].items():
            self.monitors[key] = {
                "PID": None,
                "NAME": key,
                "DRIVER": None,
                "THREAD": None,

                "monitor-description": item["PROPERTIES"][".DESCRIPTION"],
                "monitor-enabled": item["PROPERTIES"][".ENABLED"],
                "monitor-x": item["PROPERTIES"][".X"],
                "monitor-y": item["PROPERTIES"][".Y"],
                   
                "size-enabled": item["PROPERTIES"]["SIZE"][".ENABLED"],
                "size-x": item["PROPERTIES"]["SIZE"][".X"],
                "size-y": item["PROPERTIES"]["SIZE"][".Y"],
                
                "DIR": item["PROPERTIES"]["DIR"]
            }
    
        """APPLICATION"""
        self.settings_general_application = {
            "application": self.settings_general["APPLICATION"]
            }

        """UPDATES"""
        self.settings_general_updates = {
            "url": self.settings_general["UPDATES"][".URL"],
            "enabled": self.settings_general["UPDATES"][".URL"]
        }

        """BLOCK"""
        self.settings_general_block = {
            "options": self.settings_general["BLOCK"][".OPTIONS"],
            "force": {
                "enabled": self.settings_general["BLOCK"][".FORCE"][".ENABLED"],
                "url": self.settings_general["BLOCK"][".FORCE"][".URL"],
            }
        }
        
        """SYSTEM"""
        self.settings_general_system = {
            "secure-exit": {
                "enabled": self.settings_general["SYSTEM"][".SECURE-EXIT"][".ENABLED"],
                "keys": self.settings_general["SYSTEM"][".SECURE-EXIT"][".KEYS"]
            },

            "secure-start": self.settings_general["SYSTEM"][".SECURE-START"],
            
            "secure-restart": {
                "enabled": self.settings_general["SYSTEM"][".SECURE-RESTART"][".ENABLED"],
                "attempts": self.settings_general["SYSTEM"][".SECURE-RESTART"][".ATTEMPTS"]   
            },

            "datetime": {
                "enabled": self.settings_general["SYSTEM"][".DATETIME"][".ENABLED"],
                "url": self.settings_general["SYSTEM"][".DATETIME"][".URL"],
                "ssl": self.settings_general["SYSTEM"][".DATETIME"][".SSL"]
            }
        }
        
        """AUTOMATION"""
        self.settings_general_automation = {
            "automation": {
                "enabled": self.settings_general["AUTOMATION"][".ENABLED"],
                "timer": self.settings_general["AUTOMATION"][".TIMER"]
            },

            "show": self.settings_general["AUTOMATION"][".TIMER"],
            "keys": self.settings_general["AUTOMATION"][".KEYS"]
        }

        """DEV"""
        self.settings_general_dev = {
            "enabled": self.settings_general["DEV"][".ENABLED"],
            "keys": self.settings_general["DEV"][".KEYS"],
            "url": self.settings_general["DEV"][".URL"]
        }

        ### STARTUP MESSAGES
        self.logger.write(["DEBUG", f"S2SLauncher {version} - criado por: Henrique Rodrigues Pereira\n\n\npressione: {self.settings_general_system['secure-exit']['keys']} para sair"])
        
        ### VARIABLES
        self.threads = []

        ### THREADS
        #threading.Thread(target=self.secure_exit).start()

        ### FUNCTIONS
        #self.secure_start()
        #self.monitor_setup()
    
    def secure_start(self):
        if self.settings_system_secure_start:
            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

    def secure_exit(self):
        while True: 
            if keyboard.is_pressed(f"{self.general_system_secure_exit['keys']}"):
                self.register.write(["INFO", f"finalizando aplicação"])

                os.system("taskkill /F /IM chrome* /T >nul 2>&1")           

    def restart(self):
        try: 
            self.register.write(["CRITICAL", f"reiniciando aplicação, aguarde.\n"])

            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

            time.sleep(0.5)

            with open("./system/session", "r") as file:
                line = file.readline()
                os.system(f"start {line}")
            
            os._exit(0)

        except Exception as err:
            self.register.write(["ERROR", f"{err}"])
            
            os._exit(0)
    
    def automation(self):
        enabled = self.general_automation["enabled"]
        timer = self.general_automation["timer"] 
        show = self.general_automation["show"]
        keys = self.general_automation["keys"]
        
        if enabled:
            try:
                for key in keys:
                    pyautogui.press(key)

                    if show:
                        self.logger.write(["DEBUG", f"{key} pressionado!"])
                        print(f"'{key}' pressed!")

                    if timer:
                        time.sleep(0.1)

            except Exception as err:
                self.register.write(["ERROR", f"{err}"])

    def monitor_manager(self, name):
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    attempts = 0

                    driver = self.monitors[name]["DRIVER"]
                    PID = driver.service.process.pid

                    driver.get(self.general_application)

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
        
    def monitor_setup(self):
        print("setup")
        try:
            for monitor in self.monitors.values():
                if monitor["monitor-enabled"]: 
                    driver = webdriver.ChromeOptions(executable_path="./driver/chromedriver.exe")

                    """SECTION-1"""
                    driver.add_experimental_option("useAutomationExtension", False)
                    driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

                    """SECTION-2"""
                    driver.add_argument(f"--user-data-dir={monitor['DIR']}")
                    driver.add_argument(f"--window-position={monitor['monitor-position-x']},{monitor['monitor-position-y']}")

                    """SECTION-3"""
                    if monitor["monitor-size-enabled"]:
                        driver.add_argument(f"--app={self.URL}")
                        driver.add_argument(f"--window-size={monitor['monitor-size-x']},{monitor['monitor-size-y']}")
                    else:
                        ### driver.add_argument("--start-fullscreen") ###
                        driver.add_argument("--kiosk")
                    
                    """SECTION-4"""
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
    application = Application()
