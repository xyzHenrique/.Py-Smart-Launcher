"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

--LINKS--
 https://chromedriver.storage.googleapis.com/index.html 

iOneWebLauncher
"""

try:
    import os, pathlib, time, threading, traceback, pyautogui, keyboard, requests

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    from informations import *

    from modules.client import ApplicationClient
    from modules.logger import ApplicationLogger
    from modules.settings import ApplicationSettings
    
    from controller import ApplicationController

except ImportError:
    print(ImportError)

with open("version", "r") as file: version = file.readline()

class Application:
    def __init__(self):

        ### MODULES 
        self.module_client = ApplicationClient()
        self.module_logger = ApplicationLogger()
        self.module_settings = ApplicationSettings()
        self.module_controller = ApplicationController()
        
        ### SETTINGS 
        self.settings_general = self.module_settings[0]
        self.settings_monitors = self.module_settings[1]

        ### MONITOR and SETTINGS
        self.monitors = dict()

        for key,item in self.settings_monitors["MONITORS"].items():
            self.monitors[key] = {
                "monitor_PID": None,
                "monitor_name": key,
                "monitor_drive": None,
                "monitor_thread": None,

                "monitor_description": item["PROPERTIES"][".DESCRIPTION"],
                "monitor_enabled": item["PROPERTIES"][".ENABLED"],
                "monitor_x": item["PROPERTIES"][".X"],
                "monitor_y": item["PROPERTIES"][".Y"],
                   
                "size_enabled": item["PROPERTIES"]["SIZE"][".ENABLED"],
                "size_x": item["PROPERTIES"]["SIZE"][".X"],
                "size_y": item["PROPERTIES"]["SIZE"][".Y"],
                
                "DIR": item["PROPERTIES"]["DIR"]
            }
        
        """APPLICATION"""
        self.settings_general_application = {
            "URL": self.settings_general[".URL"]
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
        print(f"{APP_INFORMATIONS['APP_NAME']} - ({APP_INFORMATIONS['APP_VERSION']}) - created by: {APP_INFORMATIONS['APP_OWNER']}")
        
        ### VARIABLES
        self.threads = []

        ### FUNCTIONS
        self.secure_start()
        self.monitor_setup()
    
    def secure_start(self):
        if self.settings_general_system["secure-start"]:
            self.application_controller.end(onlychrome=True)

    def secure_exit(self):
        while self.settings_general_system["secure-exit"]["enabled"]:
            if keyboard.is_pressed(f"{self.settings_general_system['secure-exit']['keys']}"):
                self.module_logger.write_file(["INFO", f"({self.settings_general_system['secure-exit']['keys']}) closing application, please wait..."])

                self.application_controller.end(onlychrome=False)
                           
    def automation(self):
        enabled = self.settings_general_automation["automation"]["enabled"]
        timer_enabled = self.settings_general_automation["timer"]["enabled"]
        timer_time = self.settings_general_automation["timer"]["time"]
        show = self.settings_general_automation["show"]
        keys = self.settings_general_automation["keys"]
        
        if enabled:
            pyautogui.press("enter")
            try:
                for key in keys:
                    pyautogui.press(key)

                    if show:
                        self.module_logger.write_file(["DEBUG", f"{key} pressed!"])
                    if timer_enabled:
                        time.sleep(timer_time)

            except Exception:
                self.module_logger.write_file(["ERROR", f"{traceback.format_exc()}"])

    def monitor_manager(self, name):
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    application_url = self.settings_general_application["application"]
                    block_enabled = self.settings_general_block["enabled"]
                    block_url = self.settings_general_block["url"]

                    driver = self.monitors[name]["monitor_driver"]
                    driver.get(application_url)
                    driver.execute_script("window.focus()")
                    driver.execute_script(f'document.title = "monitor {name}"')

                    self.monitors[name]["monitor_PID"] = driver.service.process.pid
                    
                    self.module_logger.write_file(["INFO", f"monitor {self.monitors[name]['NAME']} ({self.monitors[name]['monitor_PID']}) OK!"])

                    self.automation()

                    i = 0
                    while True:
                        if self.settings_general_dev["enabled"]:
                            driver.execute_script(f'document.title = "DEV - {name}"')

                            if keyboard.is_pressed(self.settings_general_dev["keys"]):
                                driver.get(self.settings_general_dev["url"])
                        else:
                            if block_enabled:
                                for blocked in block_url:
                                    if driver.current_url == blocked or not driver.current_url == application_url:
                                        i += 1

                                        self.module_logger.write_file(["WARNING", f"Invalid URL running on monitor: ({name}) - ({driver.current_url}), corrections: ({i})"])
                                        
                                        pyautogui.press("f5")
                                        
                                        driver.get(application_url)
                                        driver.execute_script(f'document.title = "monitor {name}"')
                                    
                                    if i >= 3:
                                        self.module_logger.write_file(["WARNING", f"the maximum number of correction attempts has been reached!"])
                                            
                                        driver.quit()

                                        self.application_controller.restart()

                    driver.quit()

        except Exception:
            driver.quit()
            self.module_logger.write_file(["WARNING", f"monitor {self.monitors[name]['NAME']} ({traceback.format_exc()})"])
            self.application_controller.restart()
        
    def monitor_setup(self):
        ### print(f"press: ({self.settings_general_system['secure-exit']['keys']}) to exit") ###

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
                        temp = f"{os.path.expanduser('~')}\AppData\Local\Temp\FxWebLauncherPath.wlpy"
                        
                        if pathlib.Path(temp):
                            ### OFFLINE STARTUP ###
                            with open(temp, "r") as f:
                                f.readline()

                            monitor["DRIVER"] = webdriver.Chrome(f"{folder}/{r.content.decode('utf-8')}/chromedriver.exe")
                        else:
                            ### ONLINE STARTUP ###
                            monitor["DRIVER"] = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver)
                        
                    except Exception:
                        folder = f"{os.path.expanduser('~')}\.wdm\drivers\chromedriver\win32"
                        
                        if os.path.isdir(folder):
                            r = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
                            if f"{folder}/{r.content.decode('utf-8')}":

                        else:
                            pass   
                            else:
                                self.module_logger.write_file(["CRITICAL", F"{traceback.format_exc()}"])

                                self.application_controller.restart() 

                    print("\n")
                    thread = threading.Thread(target=self.monitor_manager, args=(monitor["NAME"]))
                    monitor["THREAD"] = thread  
                    thread.start()
                
                else:
                    self.module_logger.write_file(["WARNING", f"monitor {monitor['NAME']} disabled!"])
        
        except Exception:
            self.module_logger.write_file(["CRITICAL", f"{traceback.format_exc()}"])

            self.application_controller.end(onlychrome=False)

Application()
