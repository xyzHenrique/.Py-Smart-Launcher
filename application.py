"""
created by: Henrique R. Pereira <https://github.com/RIick-013>

application.py
"""

try:
    import time, threading, traceback, pyautogui, keyboard

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    from modules.settings import ApplicationSettings
    ###from modules.plugins import ApplicationPlugins
    from modules.logger import ApplicationLogger
    from controller import ApplicationController

except ImportError:
    print(ImportError)

with open("version", "r") as file: version = file.readline()

class Application:
    def __init__(self):
        self.application_logger = ApplicationLogger()
        ###self.application_plugins = ApplicationPlugins()
        self.application_settings = ApplicationSettings()
        self.application_controller = ApplicationController()
        
        self.settings_general, self.settings_monitors = self.application_settings[0], self.application_settings[1]

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

        """BLOCK"""
        self.settings_general_block = {
            "enabled": self.settings_general["BLOCK"][".ENABLED"],
            "url": self.settings_general["BLOCK"][".URL"]
        }
        
        """SYSTEM"""
        self.settings_general_system = {
            "secure-exit": {
                "enabled": self.settings_general["SYSTEM"][".SECURE-EXIT"][".ENABLED"],
                "keys": self.settings_general["SYSTEM"][".SECURE-EXIT"][".KEYS"]
            },

            "secure-start": self.settings_general["SYSTEM"][".SECURE-START"]
        }
        
        """AUTOMATION"""
        self.settings_general_automation = {
            "automation": {
                "enabled": self.settings_general["AUTOMATION"][".ENABLED"],
            },

            "timer": {
                "enabled": self.settings_general["AUTOMATION"][".TIMER"][".ENABLED"],
                "time": self.settings_general["AUTOMATION"][".TIMER"][".TIME"]
            },

            "show": self.settings_general["AUTOMATION"][".SHOW"],
            "keys": self.settings_general["AUTOMATION"][".KEYS"]
        }

        """DEV"""
        self.settings_general_dev = {
            "enabled": self.settings_general["DEV"][".ENABLED"],
            "keys": self.settings_general["DEV"][".KEYS"],
            "url": self.settings_general["DEV"][".URL"]
        }

        ### STARTUP MESSAGES
        print(f"S2SLauncher {version} - criado por: Henrique Rodrigues Pereira\n\n\npressione: {self.settings_general_system['secure-exit']['keys']} para sair")
        
        ### VARIABLES
        self.threads = []

        ### FUNCTIONS
        threading.Thread(target=self.secure_exit).start()
        self.secure_start()
        self.monitor_setup()
    
    def secure_start(self):
        if self.settings_general_system["secure-start"]:
            self.application_controller.end(onlychrome=True)

    def secure_exit(self):
        while self.settings_general_system["secure-exit"]["enabled"]:
            if keyboard.is_pressed(f"{self.settings_general_system['secure-exit']['keys']}"):
                self.application_logger.write_file(["INFO", f"({self.settings_general_system['secure-exit']['keys']}) finalizando a aplicação..."])

                time.sleep(1)

                self.application_controller.end(onlychrome=True)
                           
    def automation(self):
        enabled = self.settings_general_automation["automation"]["enabled"]
        timer_enabled = self.settings_general_automation["timer"]["enabled"]
        timer_time = self.settings_general_automation["timer"]["time"]
        show = self.settings_general_automation["show"]
        keys = self.settings_general_automation["keys"]
        
        if enabled:
            try:
                for key in keys:
                    pyautogui.press(key)

                    if show:
                        self.application_logger.write_file(["DEBUG", f"{key} pressionado!"])
                    if timer_enabled:
                        time.sleep(timer_time)

            except Exception:
                self.application_logger.write_file(["ERROR", f"{traceback.format_exc()}"])

    def monitor_manager(self, name):
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    application_url = self.settings_general_application["application"]
                    block_enabled = self.settings_general_block["enabled"]
                    block_url = self.settings_general_block["url"]
                   
                    driver = self.monitors[name]["DRIVER"]
                  
                    PID = driver.service.process.pid

                    driver.get(application_url)

                    self.application_logger.write_file(["INFO", f"monitor {self.monitors[name]['NAME']} ({PID}) criado!"])
                    
                    ### ============== ###
                    ### FIX TASKBAR
                    pyautogui.press("enter")
                    time.sleep(.1)
                    ### ============== ###

                    self.automation()

                    driver.execute_script(f'document.title = "monitor {name}"')

                    i = 0
                    while True:
                        if block_enabled:
                            for blocked in block_url:
                                if driver.current_url == blocked or not driver.current_url == application_url:
                                    i += 1

                                    self.application_logger.write_file(["WARNING", f"uma ULR inválida está sendo executada no monitor {name} - ({driver.current_url}), tentativas de correção: ({i})"])
                                    
                                    pyautogui.press("f5")
                                    
                                    driver.get(application_url)
                                    driver.execute_script(f'document.title = "monitor {name}"')
                                
                                if i >= 3:
                                    self.application_logger.write_file(["WARNING", f"o número máximo de tentativas de correções foi atingido (3)"])
                                        
                                    driver.quit()

                                    self.application_controller.restart()

                        if self.settings_general_dev["enabled"]:
                            driver.execute_script(f'document.title = "DEV - {name}"')

                            if keyboard.is_pressed(self.settings_general_dev["keys"]):
                                driver.get(self.settings_general_dev["url"])

                        time.sleep(1)

        except Exception:
            self.application_logger.write_file(["WARNING", f"monitor {self.monitors[name]['NAME']} ({traceback.format_exc()})"])
            self.application_controller.restart()
        
    def monitor_setup(self):
        try:
            for monitor in self.monitors.values():
                if monitor["monitor-enabled"]: 
                    driver = webdriver.ChromeOptions()

                    """SECTION-1"""
                    driver.add_experimental_option("useAutomationExtension", False)
                    driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

                    """SECTION-2"""
                    driver.add_argument(f"--user-data-dir={monitor['DIR']}")
                    driver.add_argument(f"--window-position={monitor['monitor-x']},{monitor['monitor-y']}")

                    """SECTION-3"""
                    if monitor["size-enabled"]:
                        driver.add_argument(f"--app={self.settings_general_application['application']}")
                        driver.add_argument(f"--window-size={monitor['size-x']},{monitor['size-y']}")
                    else:
                        driver.add_argument("--kiosk")
                    
                    """SECTION-4"""
                    driver.add_argument("--test-type")
                    driver.add_argument("--new-window")
                    driver.add_argument("--unlimited-storage")
                    driver.add_argument("--disable-extensions")                
                    driver.add_argument("--disable-notifications")
                    driver.add_argument("--ignore-certificate-errors")
                    driver.add_argument("--autoplay-policy=no-user-gesture-required")
                    driver.add_argument("--disable-features=ChromeWhatsNewUI")
                    
                    """SECTION-5"""
                    try:
                        monitor["DRIVER"] = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver)
                    except Exception:
                        self.application_logger.write_file(["CRITICAL", F"{traceback.format_exc()}"])

                        self.application_controller.restart() 

                    print("\n")
                    thread = threading.Thread(target=self.monitor_manager, args=(monitor["NAME"]))
                    monitor["THREAD"] = thread  
                    thread.start()
                
                else:
                    self.application_logger.write_file(["WARNING", f"monitor {monitor['NAME']} está desabilitado!"])
        
        except Exception:
            self.application_logger.write_file(["CRITICAL", f"{traceback.format_exc()}"])

            self.application_controller.end(onlychrome=False)

Application()
